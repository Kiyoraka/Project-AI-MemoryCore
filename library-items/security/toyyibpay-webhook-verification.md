# ToyyibPay Webhook Verification
*Secure callback handling for the ToyyibPay Malaysian payment gateway*

## Threat Model
- **Threat**: forged webhook callbacks, replayed callbacks, unauthorized payment confirmations
- **Impact**: fraudulent order fulfilment, goods shipped or services granted without payment, financial loss
- **Severity**: Critical

## Use Case
- Malaysian e-commerce applications
- Booking systems taking FPX or card payments
- Subscription and instalment payment processing
- Any application whose fulfilment is triggered by a ToyyibPay callback

## Why This Pattern Exists

Unlike gateways that sign their webhooks (Stripe's HMAC `Stripe-Signature` header, for example),
**ToyyibPay sends no cryptographic signature**. The callback is a plain form POST to a URL that must
be publicly reachable and cannot require auth. Anyone who learns that URL can POST
`billcode=X&status_id=1` to it.

The only trustworthy signal is ToyyibPay's own API. So the rule is simple:

> Never trust the callback body. Treat it as a *notification that something happened*, then re-ask
> the API what actually happened.

## Verification Flow

Framework-neutral — implement these seven steps in whatever stack you use.

1. **Log the raw request first** (IP, timestamp, full payload) before any parsing, so a malformed or
   hostile callback is still forensically visible.
2. **Reject callbacks missing `billcode`** with HTTP 400. Nothing downstream can proceed without it.
3. **Call `getBillTransactions` with that bill code** — a fresh server-to-server request to
   ToyyibPay. This is the verification step; everything before it is untrusted input.
4. **Confirm a transaction with `billpaymentStatus == "1"` exists** in the response. If not, the
   callback is unverified — refuse it.
5. **Cross-check the amount** against your own order record before fulfilling. A verified bill code
   still tells you nothing about whether the amount matches what you charged.
6. **Check idempotency** — if this bill code is already marked paid, return 200 and stop. ToyyibPay
   retries callbacks, and duplicate fulfilment is a real loss.
7. **Wrap fulfilment in a database transaction** and return HTTP 200 only after commit. Return a
   non-2xx on internal failure so the retry is allowed to happen.

## Implementation

### Backend — Webhook Controller

```php
<?php
// app/Http/Controllers/ToyyibPayWebhookController.php

namespace App\Http\Controllers;

use App\Models\Order;
use App\Services\ToyyibPayService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class ToyyibPayWebhookController extends Controller
{
    public function __construct(
        private ToyyibPayService $toyyibPayService
    ) {}

    public function handle(Request $request)
    {
        // 1. Log incoming webhook before parsing anything
        Log::info('ToyyibPay Webhook Received', [
            'ip'        => $request->ip(),
            'timestamp' => now()->toISOString(),
            'data'      => $request->all(),
        ]);

        // 2. Extract callback data
        $callbackData = [
            'billcode'       => $request->input('billcode'),
            'status_id'      => $request->input('status_id'),
            'order_id'       => $request->input('order_id'),
            'transaction_id' => $request->input('transaction_id'),
            'msg'            => $request->input('msg'),
            'reason'         => $request->input('reason'),
        ];

        // 3. Validate required fields
        if (empty($callbackData['billcode'])) {
            Log::warning('ToyyibPay callback missing billcode', $callbackData);
            return response()->json(['status' => 'error', 'message' => 'Missing billcode'], 400);
        }

        // 4. CRITICAL: verify the callback against the ToyyibPay API
        if (!$this->toyyibPayService->verifyCallback($callbackData)) {
            Log::warning('ToyyibPay callback verification FAILED', $callbackData);
            return response()->json(['status' => 'error', 'message' => 'Invalid callback'], 400);
        }

        // 5. Check payment outcome. status_id: 1 = Success, 2 = Pending, 3 = Failed
        if ($callbackData['status_id'] != '1') {
            Log::info('ToyyibPay payment not successful', [
                'billcode'  => $callbackData['billcode'],
                'status_id' => $callbackData['status_id'],
                'reason'    => $callbackData['reason'] ?? 'Unknown',
            ]);
            return response()->json(['status' => 'ok', 'message' => 'Payment not successful']);
        }

        // 6. Process payment inside a database transaction
        DB::beginTransaction();
        try {
            $this->processPayment($callbackData);
            DB::commit();

            Log::info('ToyyibPay payment processed successfully', [
                'billcode' => $callbackData['billcode'],
            ]);

            return response()->json(['status' => 'ok']);
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('ToyyibPay payment processing failed', [
                'billcode' => $callbackData['billcode'],
                'error'    => $e->getMessage(),
            ]);
            // Non-2xx so ToyyibPay is allowed to retry
            return response()->json(['status' => 'error'], 500);
        }
    }

    private function processPayment(array $callbackData): void
    {
        $order = Order::where('toyyibpay_bill_code', $callbackData['billcode'])->first();

        if (!$order) {
            Log::warning('Verified callback for unknown bill code', [
                'billcode' => $callbackData['billcode'],
            ]);
            return;
        }

        // Idempotency check — ToyyibPay retries, and duplicate fulfilment is a real loss
        if ($order->payment_status === 'paid') {
            Log::info('Payment already processed (idempotency)', [
                'billcode' => $callbackData['billcode'],
                'order_id' => $order->id,
            ]);
            return;
        }

        $order->update([
            'payment_status'           => 'paid',
            'payment_date'             => now(),
            'toyyibpay_transaction_id' => $callbackData['transaction_id'],
        ]);

        // Your post-payment business logic here
        // (fulfilment, receipt email, loyalty points, notifications, stock decrement...)
    }
}
```

### Backend — Service Verification Method

```php
<?php
// app/Services/ToyyibPayService.php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class ToyyibPayService
{
    private string $secretKey;
    private string $categoryCode;
    private string $baseUrl;

    public function __construct()
    {
        // Credentials shown here from config/env for brevity. If merchants manage their own
        // keys from an admin panel, swap these three lines for the encrypted PaymentSetting
        // model in the companion integration item — nothing below this constructor changes.
        $this->secretKey    = config('services.toyyibpay.secret_key');
        $this->categoryCode = config('services.toyyibpay.category_code');
        $this->baseUrl      = config('services.toyyibpay.test_mode')
            ? 'https://dev.toyyibpay.com'
            : 'https://toyyibpay.com';
    }

    /**
     * Verify a callback by asking ToyyibPay directly about the transaction.
     * This is the whole security model — the callback body itself proves nothing.
     */
    public function verifyCallback(array $callbackData): bool
    {
        try {
            $billCode = $callbackData['billcode'];

            $response = Http::timeout(30)->asForm()
                ->post("{$this->baseUrl}/index.php/api/getBillTransactions", [
                    'billCode' => $billCode,
                ]);

            if (!$response->successful()) {
                Log::warning('ToyyibPay API call failed', [
                    'billcode' => $billCode,
                    'status'   => $response->status(),
                ]);
                return false;
            }

            $transactions = $response->json();

            if (empty($transactions) || !is_array($transactions)) {
                Log::warning('No transactions found for billcode', ['billcode' => $billCode]);
                return false;
            }

            // billpaymentStatus: 1 = Success, 2 = Pending, 3 = Failed
            foreach ($transactions as $transaction) {
                if (isset($transaction['billpaymentStatus'])
                    && $transaction['billpaymentStatus'] === '1') {
                    return true;
                }
            }

            Log::warning('No successful transaction found', ['billcode' => $billCode]);
            return false;

        } catch (\Exception $e) {
            Log::error('ToyyibPay verification exception', [
                'error'    => $e->getMessage(),
                'billcode' => $callbackData['billcode'] ?? 'unknown',
            ]);
            return false;
        }
    }

    /**
     * Create a bill. Secret key is masked before any logging.
     * $params['amount'] is in RINGGIT — converted to cents below.
     */
    public function createBill(array $params): ?array
    {
        try {
            // Never log credentials, even indirectly
            $logParams = $params;
            if (isset($logParams['userSecretKey'])) {
                $logParams['userSecretKey'] = '***MASKED***';
            }
            Log::info('Creating ToyyibPay bill', $logParams);

            $amountInCents = (int) round($params['amount'] * 100);

            $response = Http::asForm()->post("{$this->baseUrl}/index.php/api/createBill", [
                'userSecretKey'           => $this->secretKey,
                'categoryCode'            => $this->categoryCode,
                'billName'                => $params['billName'],
                'billDescription'         => $params['billDescription'],
                'billPriceSetting'        => 1,   // fixed amount
                'billPayorInfo'           => 1,   // pre-fill payer form
                'billAmount'              => $amountInCents,  // cents, integer, min 100
                'billReturnUrl'           => $params['returnUrl'],
                'billCallbackUrl'         => $params['callbackUrl'],
                'billExternalReferenceNo' => $params['referenceNo'],
                'billTo'                  => $params['customerName'],
                'billEmail'               => $params['customerEmail'],
                'billPhone'               => $params['customerPhone'],
                'billPaymentChannel'      => $params['paymentChannel'] ?? '2',  // 0=FPX, 1=Card, 2=Both
            ]);

            if ($response->successful()) {
                $result = $response->json();

                if (isset($result[0]['BillCode'])) {
                    $billCode = $result[0]['BillCode'];

                    Log::info('ToyyibPay bill created', [
                        'billcode'  => $billCode,
                        'reference' => $params['referenceNo'],
                    ]);

                    return [
                        'bill_code'   => $billCode,
                        'payment_url' => "{$this->baseUrl}/{$billCode}",
                    ];
                }
            }

            Log::error('ToyyibPay bill creation failed', [
                'response' => $response->body(),
            ]);
            return null;

        } catch (\Exception $e) {
            Log::error('ToyyibPay createBill exception', [
                'error' => $e->getMessage(),
            ]);
            return null;
        }
    }
}
```

### Middleware — IP Allowlist (Optional, Defence in Depth)

```php
<?php
// Middleware to verify the webhook source IP

public function handle(Request $request, Closure $next)
{
    $allowedIps = config('services.toyyibpay.allowed_ips', []);

    // No allowlist configured — fall through to API-side verification only
    if (empty($allowedIps)) {
        return $next($request);
    }

    $requestIp = $request->ip();

    foreach ($allowedIps as $allowedIp) {
        if ($this->ipInRange($requestIp, $allowedIp)) {
            return $next($request);
        }
    }

    Log::warning('Webhook from unauthorized IP', ['ip' => $requestIp]);
    return response()->json(['error' => 'Unauthorized'], 403);
}
```

> **Caveat**: ToyyibPay does not officially publish its outbound callback IP ranges, and they can
> change without notice. Confirm the current ranges with ToyyibPay support before enabling this, keep
> them in config rather than hardcoded, and never let an allowlist *replace* the API verification in
> step 3 — it is a second lock on the same door, not the door.

### Route Configuration

```php
<?php
// routes/api.php

use App\Http\Controllers\ToyyibPayWebhookController;

// Webhook route — NO auth middleware, NO CSRF (ToyyibPay cannot supply either)
Route::post('/toyyibpay/callback', [ToyyibPayWebhookController::class, 'handle'])
    ->name('toyyibpay.callback');
```

### Database — Bill Code Uniqueness

A unique constraint is what makes idempotency safe under concurrent retries. A read-then-write check
alone is a race: two simultaneous callbacks can both read "not yet paid" and both fulfil.

```php
// Migration
Schema::table('orders', function (Blueprint $table) {
    $table->string('toyyibpay_bill_code')->nullable()->unique();
    $table->string('toyyibpay_transaction_id')->nullable();
    $table->timestamp('payment_date')->nullable();
});
```

## Configuration

### Environment Variables

```env
# Production
TOYYIBPAY_SECRET_KEY=your-secret-key
TOYYIBPAY_CATEGORY_CODE=your-category-code
TOYYIBPAY_TEST_MODE=false

# Development / Testing
TOYYIBPAY_SECRET_KEY=your-sandbox-key
TOYYIBPAY_CATEGORY_CODE=your-sandbox-category
TOYYIBPAY_TEST_MODE=true
```

### Config File

```php
<?php
// config/services.php

return [
    'toyyibpay' => [
        'secret_key'    => env('TOYYIBPAY_SECRET_KEY'),
        'category_code' => env('TOYYIBPAY_CATEGORY_CODE'),
        'test_mode'     => env('TOYYIBPAY_TEST_MODE', false),
        'allowed_ips'   => array_filter(explode(',', env('TOYYIBPAY_ALLOWED_IPS', ''))),
    ],
];
```

## Validation Rules
- Every callback must carry a non-empty `billcode` — reject with 400 otherwise
- Payment is confirmed only by a `billpaymentStatus == "1"` from `getBillTransactions`, never by the
  callback's own `status_id`
- The verified amount must match the stored order total before fulfilment
- `toyyibpay_bill_code` must carry a database-level unique constraint
- The callback endpoint must be publicly reachable over HTTPS with no auth or CSRF middleware
- The secret key must never appear in logs, error messages or responses

## Error Responses

| Scenario | Response |
|----------|----------|
| Missing `billcode` | `400` `{"status":"error","message":"Missing billcode"}` |
| API verification failed | `400` `{"status":"error","message":"Invalid callback"}` |
| Payment not successful (`status_id` 2 or 3) | `200` `{"status":"ok","message":"Payment not successful"}` |
| Unknown bill code (verified but no matching order) | `200` `{"status":"ok"}` + warning log |
| Already processed (idempotent replay) | `200` `{"status":"ok"}` |
| Internal failure during fulfilment | `500` `{"status":"error"}` — allows ToyyibPay to retry |

## ToyyibPay Status Codes

| Status ID | Meaning | Action |
|-----------|---------|--------|
| `1` | Payment successful | Verify, then fulfil |
| `2` | Payment pending | Wait for a later callback |
| `3` | Payment failed | Notify the customer, keep the order unpaid |

## Callback Data Structure

```php
// ToyyibPay sends this POST data
[
    'refno'            => 'TP123456',            // ToyyibPay reference
    'status'           => '1',                   // Payment status
    'reason'           => 'Approved',            // Status reason
    'billcode'         => 'abc123xyz',           // Your bill code
    'order_id'         => 'ORD-001',             // Your external reference
    'amount'           => '10000',               // Amount in cents (RM 100.00)
    'transaction_time' => '2026-01-18 12:00:00',
]
```

## Testing

### Test Cases
- **Verified success**: valid bill code + successful API transaction → order marked paid, HTTP 200
- **Forged callback**: `status_id=1` for a bill code with no successful transaction → HTTP 400, order untouched
- **Replay**: the same successful callback delivered twice → fulfilment runs once, both return 200
- **Missing billcode**: HTTP 400, nothing written
- **API unreachable during verification**: verification returns false → HTTP 400, order untouched
- **Amount mismatch**: verified bill whose amount differs from the order total → refuse fulfilment

### Webhook Simulation

```php
public function test_webhook_processes_successful_payment()
{
    // Mock the ToyyibPay verification API
    Http::fake([
        'toyyibpay.com/*' => Http::response([[
            'billpaymentStatus' => '1',
        ]]),
    ]);

    $order = Order::factory()->create([
        'toyyibpay_bill_code' => 'TEST123',
        'payment_status'      => 'pending',
    ]);

    $response = $this->postJson('/api/toyyibpay/callback', [
        'billcode'       => 'TEST123',
        'status_id'      => '1',
        'transaction_id' => 'TXN123',
    ]);

    $response->assertOk();
    $this->assertEquals('paid', $order->fresh()->payment_status);
}

public function test_webhook_rejects_unverified_callback()
{
    Http::fake([
        'toyyibpay.com/*' => Http::response([]),  // Empty = no transaction exists
    ]);

    $response = $this->postJson('/api/toyyibpay/callback', [
        'billcode'  => 'FAKE123',
        'status_id' => '1',
    ]);

    $response->assertStatus(400);
}
```

### Security Audit Checklist
- [ ] Webhook verifies every payment via a server-side API call
- [ ] Callback `status_id` alone never triggers fulfilment
- [ ] Verified amount is cross-checked against the stored order total
- [ ] Bill codes have a unique database constraint
- [ ] Idempotency prevents duplicate processing under retries
- [ ] Fulfilment is wrapped in a database transaction
- [ ] Failed webhooks are logged with full detail
- [ ] Secret key is masked in all logs
- [ ] Return and callback URLs use HTTPS
- [ ] Callback URL is publicly accessible with no auth/CSRF middleware
- [ ] IP allowlist (if used) is config-driven and treated as defence in depth only

## Logging & Monitoring

**What to log**
- Every inbound callback: source IP, timestamp, full payload — before parsing
- Every verification outcome, pass or fail, with the bill code
- Every state change: bill code, order id, amount, transaction id, timestamp

```php
Log::info('ToyyibPay Payment Success', [
    'billcode'       => $callbackData['billcode'],
    'order_id'       => $order->id,
    'amount'         => $order->total_amount,
    'customer_id'    => $order->user_id,
    'transaction_id' => $callbackData['transaction_id'],
    'timestamp'      => now()->toISOString(),
]);
```

**Alert conditions**
- Any verification failure — a single one may be a probe
- Repeated callbacks for bill codes that do not exist in your database
- Callbacks arriving from unexpected source IPs
- A spike in duplicate callbacks for the same bill code

**Audit trail**: retain callback logs long enough to reconcile against merchant settlement reports,
and keep them immutable — payment disputes are settled with them.

## Comparison with Other Gateways

| Feature | ToyyibPay | Stripe | Billplz |
|---------|-----------|--------|---------|
| Verification method | API callback | HMAC signature | API callback |
| Signature header | None | `Stripe-Signature` | `X-Billplz-Signature` |
| Idempotency | Manual | Built-in | Manual |
| Test environment | dev.toyyibpay.com | Sandbox keys | sandbox.billplz.com |

## See Also
- `integration/toyyibpay-payment-gateway` — bill creation, API contract, credential test, and the
  known ToyyibPay API gotchas

Both items sketch a `ToyyibPayService`. If you install both, merge them into a single class — this
one contributes `verifyCallback()` and the masked-logging `createBill()`; the integration item
contributes `getBill()`, `isPaid()` and `testConnection()`. Both take `amount` in ringgit and convert
to cents internally, so the signatures already agree.

## Projects Using This
- *(Add your projects here after implementing)*

---
*Documented: July 2026*
*Pattern: API-callback verification for gateways that ship no webhook signature*
