# ToyyibPay Payment Gateway Integration
*Malaysian FPX & credit card payment gateway — bill creation, callbacks, and credential validation*

## Service Info
- **Provider**: ToyyibPay Sdn Bhd (Malaysia)
- **Type**: REST API with webhook callbacks
- **Documentation**: https://toyyibpay.com/apireference
- **Payment Methods**: FPX (online banking), credit card, corporate banking (FPX B2B)

## Use Case
- Malaysian online payments via FPX (the most widely used local method)
- Credit card processing
- Corporate/business banking (FPX B2B)
- E-commerce checkout integration
- Subscription or instalment billing via bill codes

## API Contract

Framework-neutral reference — everything below works the same from any stack. All calls are
`POST` with `Content-Type: application/x-www-form-urlencoded`.

**Base URL**: `https://toyyibpay.com/` (production) or `https://dev.toyyibpay.com/` (sandbox)

| Endpoint | Required params | Returns |
|----------|-----------------|---------|
| `index.php/api/createBill` | `userSecretKey`, `categoryCode`, `billName`, `billDescription`, `billPriceSetting`, `billPayorInfo`, `billAmount`, `billReturnUrl`, `billCallbackUrl`, `billExternalReferenceNo`, `billTo`, `billEmail`, `billPhone` | `[{"BillCode":"..."}]` on success, `{"status":"error","msg":"..."}` on failure |
| `index.php/api/getBillTransactions` | `billCode` (optionally `userSecretKey`) | Array of transaction objects with `billpaymentStatus`, `billpaymentChannel`, `billpaymentDate` |
| `index.php/api/getCategoryDetails` | `userSecretKey`, `categoryCode` | Category object on success, literal text `[FALSE]` on invalid credentials |
| `GET /{BillCode}` | — | Hosted payment page the customer is redirected to |

**Key field semantics**

| Field | Values |
|-------|--------|
| `billPriceSetting` | `1` = fixed amount, `0` = customer enters amount |
| `billPayorInfo` | `1` = pre-fill payer fields from `billTo`/`billEmail`/`billPhone`, `0` = blank form (see Common Pitfalls) |
| `billPaymentChannel` | `0` = FPX, `1` = credit card, `2` = both |
| `enableFPXB2B` | `1` = enable corporate banking |
| `chargeFPXB2B` | `0` = customer pays the fee, `1` = merchant pays |
| `billpaymentStatus` (response) | `1` = success, `2` = pending, `3` = failed |
| `status_id` (callback) | `1` = success, `2` = pending, `3` = failed |

## Porting Notes

Three traps that are independent of your language or framework. Every one of them has bitten a
first implementation:

1. **Amounts are in cents, as an integer.** `RM 342.00` is sent as `34200`, not `342` and not
   `342.00`. Minimum is `100` (RM 1.00). Sending ringgit instead of cents silently charges 1/100
   of the intended amount.
2. **Failures come back as HTTP 200.** ToyyibPay signals errors in the body, never in the status
   code. Worse, invalid credentials on `getCategoryDetails` return the **literal text `[FALSE]`**,
   which is not JSON — decode it and your parser throws or yields null. Always inspect the raw body
   before decoding.
3. **`getCategoryDetails` returns `CategoryName` with a capital C** while its sibling keys are
   lowercase (`categoryDescription`, `categoryStatus`). JSON keys are case-sensitive, so a parser
   that guesses the consistent lowercase spelling silently misses the value. Values also carry
   trailing whitespace — trim before displaying.

A fourth, softer one: responses are sometimes a bare object and sometimes an array-wrapped object.
Handle both shapes rather than assuming one.

## Configuration

Two ways to hold credentials — pick one before you write any code, because it decides who can change
the keys without a deploy.

| Approach | Use when | Trade-off |
|----------|----------|-----------|
| **Admin settings in the database** (`PaymentSetting` below — used by the service class in this item) | The merchant owns their own ToyyibPay account and must be able to paste keys, flip sandbox/production and test the connection from an admin screen | Needs encryption at rest and an admin UI, but no redeploy to change keys or switch modes |
| **Environment variables** | You operate the ToyyibPay account yourself and keys change roughly never | Simplest, but every key rotation or mode switch is a deploy, and non-developers cannot do it |

The service class in this item reads from `PaymentSetting`. To go env-only instead, replace the
constructor's three lookups with `config('services.toyyibpay.*')` — nothing else changes.

### Environment Variables
```env
TOYYIBPAY_SECRET_KEY=your_secret_key
TOYYIBPAY_CATEGORY_CODE=your_category_code
TOYYIBPAY_MODE=sandbox  # or production
```

### Config File
```php
<?php
// config/services.php

return [
    'toyyibpay' => [
        'secret_key'    => env('TOYYIBPAY_SECRET_KEY'),
        'category_code' => env('TOYYIBPAY_CATEGORY_CODE'),
        'mode'          => env('TOYYIBPAY_MODE', 'sandbox'),
    ],
];
```

### Database Model — PaymentSetting (admin-managed credentials)

The admin-settings path. Merchants paste their own `userSecretKey` and `categoryCode` into an admin
screen; both are encrypted at rest, the `mode` column flips sandbox/production without a deploy, and
the Test Connection diagnostic further down validates the saved pair before any real bill is created.

Never render the saved secret back into the admin form — show a masked placeholder and only write the
field when the merchant submits a new value.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Crypt;

class PaymentSetting extends Model
{
    protected $fillable = [
        'gateway',
        'mode',           // sandbox | production
        'secret_key',     // userSecretKey (encrypted at rest)
        'collection_id',  // categoryCode (encrypted at rest)
        'is_active',
    ];

    // Encrypt on set
    public function setSecretKeyAttribute($value)
    {
        if ($value) {
            $this->attributes['secret_key'] = Crypt::encryptString($value);
        }
    }

    // Decrypt on get
    public function getSecretKeyAttribute($value)
    {
        return $value ? Crypt::decryptString($value) : null;
    }

    // API URL based on mode
    public function getApiUrl(): string
    {
        return $this->mode === 'sandbox'
            ? 'https://dev.toyyibpay.com/'
            : 'https://toyyibpay.com/';
    }

    public static function getByGateway(string $gateway): ?self
    {
        return self::where('gateway', $gateway)
            ->where('is_active', true)
            ->first();
    }
}
```

## Implementation

### Backend Service Class

The service takes an explicit parameter array rather than reaching into your domain models, so it
drops into any schema unchanged.

```php
<?php

namespace App\Services;

use App\Models\PaymentSetting;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class ToyyibPayService
{
    protected $settings;
    protected string $apiUrl;

    public function __construct()
    {
        $this->settings = PaymentSetting::getByGateway('toyyibpay');

        if (!$this->settings) {
            throw new \Exception('ToyyibPay payment gateway is not configured or inactive');
        }

        $this->apiUrl = $this->settings->getApiUrl();
    }

    /**
     * Create a payment bill.
     *
     * @param array $params {
     *   @type float  $amount         Amount in RINGGIT — converted to cents below
     *   @type string $referenceNo    Your unique order reference
     *   @type string $description    Shown on the payment page
     *   @type string $customerName   Pre-fills the payer form
     *   @type string $customerEmail  Pre-fills the payer form (required for online payment)
     *   @type string $customerPhone  Pre-fills the payer form, format 0123456789
     *   @type string $returnUrl      Where the customer lands after paying
     *   @type string $callbackUrl    Server-to-server webhook endpoint
     *   @type string $paymentChannel 0=FPX, 1=Card, 2=Both (default 0)
     * }
     */
    public function createBill(array $params): array
    {
        try {
            // Convert to cents — CRITICAL, see Porting Notes
            $amountInCents = (int) round($params['amount'] * 100);

            $billData = [
                'userSecretKey'            => $this->settings->secret_key,
                'categoryCode'             => $this->settings->collection_id,
                'billName'                 => substr($params['referenceNo'], 0, 30),  // max 30 chars
                'billDescription'          => $params['description'],
                'billPriceSetting'         => 1,   // 1 = fixed amount
                'billPayorInfo'            => 1,   // 1 = pre-fill payer form (see Common Pitfalls)
                'billAmount'               => $amountInCents,
                'billReturnUrl'            => $params['returnUrl'],
                'billCallbackUrl'          => $params['callbackUrl'],
                'billExternalReferenceNo'  => $params['referenceNo'],
                'billTo'                   => $params['customerName'],
                'billEmail'                => $params['customerEmail'],
                'billPhone'                => $params['customerPhone'],
                'billPaymentChannel'       => $params['paymentChannel'] ?? '0',
                'enableFPXB2B'             => '1',  // corporate banking
                'chargeFPXB2B'             => '0',  // 0 = customer pays the fee
            ];

            $response = Http::timeout(30)
                ->asForm()
                ->post($this->apiUrl . 'index.php/api/createBill', $billData);

            if ($response->failed()) {
                throw new \Exception('Failed to create payment bill: ' . $response->body());
            }

            $billResponse = $response->json();

            // Error responses arrive with HTTP 200 — check the body
            if (isset($billResponse['status']) && $billResponse['status'] === 'error') {
                throw new \Exception('ToyyibPay Error: ' . ($billResponse['msg'] ?? 'Unknown'));
            }

            // Success shape is an array: [0]['BillCode']
            if (!isset($billResponse[0]['BillCode'])) {
                throw new \Exception('Invalid response - Missing BillCode');
            }

            $billCode = $billResponse[0]['BillCode'];

            return [
                'BillCode'    => $billCode,
                'payment_url' => $this->apiUrl . $billCode,
                'bill_data'   => $billResponse[0],
            ];

        } catch (\Exception $e) {
            Log::error('ToyyibPay Service Error', [
                'message'   => $e->getMessage(),
                'reference' => $params['referenceNo'] ?? null,
            ]);
            throw $e;
        }
    }

    /**
     * Get bill transaction details.
     */
    public function getBill(string $billCode): array
    {
        $response = Http::timeout(30)
            ->asForm()
            ->post($this->apiUrl . 'index.php/api/getBillTransactions', [
                'billCode'      => $billCode,
                'userSecretKey' => $this->settings->secret_key,
            ]);

        if ($response->failed()) {
            throw new \Exception('Failed to retrieve bill information');
        }

        return $response->json();
    }

    /**
     * Check payment status.
     * billpaymentStatus: 1=Success, 2=Pending, 3=Failed
     */
    public function isPaid(array $billData): bool
    {
        return isset($billData[0]['billpaymentStatus'])
            && $billData[0]['billpaymentStatus'] == '1';
    }

    public function getPaymentMethod(array $billData): ?string
    {
        return $billData[0]['billpaymentChannel'] ?? null;
    }

    public function getPaidAt(array $billData): ?string
    {
        return $billData[0]['billpaymentDate'] ?? null;
    }
}
```

### Controller — Checkout

```php
/**
 * Start a payment: create the bill, store the code, redirect to the hosted page.
 */
public function checkout(Request $request, ToyyibPayService $toyyibPay)
{
    $order = Order::findOrFail($request->input('order_id'));

    $bill = $toyyibPay->createBill([
        'amount'         => $order->total_amount,
        'referenceNo'    => $order->order_number,
        'description'    => "Order #{$order->order_number}",
        'customerName'   => $order->customer_name,
        'customerEmail'  => $order->customer_email,
        'customerPhone'  => $this->normalizePhone($order->customer_phone),
        'returnUrl'      => url("/payment/success?order_id={$order->id}"),
        'callbackUrl'    => url('/api/webhooks/toyyibpay'),
        'paymentChannel' => '2',  // FPX + card
    ]);

    $order->update(['payment_reference' => $bill['BillCode']]);

    return redirect()->away($bill['payment_url']);
}
```

### Controller — Webhook Callback

Minimal handler. For the hardened version — API-side verification, idempotency, IP allowlist and an
audit checklist — install the companion item (see **See Also**).

```php
/**
 * ToyyibPay webhook callback.
 * Route: POST /api/webhooks/toyyibpay  (no auth, no CSRF)
 */
public function toyyibpayCallback(Request $request)
{
    Log::info('ToyyibPay Callback', ['data' => $request->all()]);

    $statusId = $request->input('status_id');
    $billCode = $request->input('billcode');
    $refNo    = $request->input('refno');   // your billExternalReferenceNo

    if (!$billCode) {
        return response('Invalid callback', 400);
    }

    $order = Order::where('payment_reference', $billCode)
        ->orWhere('order_number', $refNo)
        ->first();

    if (!$order) {
        return response('Order not found', 404);
    }

    // Status: 1=Success, 2=Pending, 3=Failed
    if ($statusId == '1') {
        $order->update(['payment_status' => 'paid', 'payment_date' => now()]);
        // Your post-payment business logic here (fulfilment, receipt, notifications...)
    } elseif ($statusId == '3') {
        $order->update(['payment_status' => 'failed']);
    }

    return response('OK', 200);
}
```

### Test Connection (getCategoryDetails)

An admin diagnostic that validates the saved `userSecretKey` + `categoryCode` **without creating a
bill**. Valid credentials return the category details; invalid ones return the literal `[FALSE]`.

```php
/**
 * Validate saved credentials against ToyyibPay.
 * Returns ['ok' => bool, 'message' => string] so the admin UI can always show a reason.
 */
public function testConnection(): array
{
    $response = Http::timeout(30)->asForm()->post($this->apiUrl . 'index.php/api/getCategoryDetails', [
        'userSecretKey' => $this->settings->secret_key,
        'categoryCode'  => $this->settings->collection_id,
    ]);

    $body = trim((string) $response->body());

    // Invalid key/category comes back as the literal text [FALSE] — NOT JSON. Check before decoding.
    if ($body === '' || strcasecmp($body, '[FALSE]') === 0) {
        return ['ok' => false, 'message' => 'Invalid Secret Key or Category Code.'];
    }

    $json = json_decode($body, true);
    if (isset($json['status']) && $json['status'] === 'error') {
        return ['ok' => false, 'message' => 'ToyyibPay error: ' . ($json['msg'] ?? 'invalid credentials')];
    }

    // ToyyibPay may return a bare object OR an array-wrapped object.
    $node = array_is_list($json ?? []) ? ($json[0] ?? null) : $json;

    // GOTCHA: the key is "CategoryName" (capital C), while its siblings are lowercase
    // (categoryDescription / categoryStatus). Read case-insensitively — never trust one spelling.
    $name = $node['CategoryName'] ?? $node['categoryName'] ?? null;
    if (is_string($name) && trim($name) !== '') {
        return ['ok' => true, 'message' => "Connected - category '" . trim($name) . "' is valid."];
    }

    return ['ok' => false, 'message' => 'Unexpected ToyyibPay response: ' . mb_substr($body, 0, 200)];
}
```

**Response shapes** (all HTTP 200 — ToyyibPay signals failure in the body, not the status code):

| Case | Body |
|------|------|
| Valid credentials | `{"CategoryName":"YOUR CATEGORY NAME ","categoryDescription":"PAYMENT ","categoryStatus":"1"}` |
| Invalid key/category | `[FALSE]` (literal text, **not JSON** — decode will fail) |
| Error object | `{"status":"error","msg":"..."}` |

Note the trailing whitespace ToyyibPay leaves inside the values (`"...NAME "`) — `trim()` the name
before displaying.

## Request/Response Examples

### Create Bill Request
```
POST https://toyyibpay.com/index.php/api/createBill
Content-Type: application/x-www-form-urlencoded

userSecretKey=xxx&categoryCode=xxx&billName=ORD-001&billAmount=34200&billPayorInfo=1...
```

### Create Bill Response (Success)
```json
[
    {
        "BillCode": "abc123xyz"
    }
]
```

### Create Bill Response (Error)
```json
{
    "status": "error",
    "msg": "Invalid category code"
}
```

### Callback Payload
```
billcode=abc123xyz
&order_id=12345
&status_id=1
&transaction_status=Completed
&refno=ORD-001
&reason=Payment successful
```

## Common Pitfalls

### `billPayorInfo` Flag Misread (Pre-fill Gotcha)

**Symptom**: The customer fills Name/Email/Phone on YOUR checkout form, gets redirected to
ToyyibPay's hosted page, and is asked to enter Name/Email/Phone AGAIN. Duplicate data entry, and it
hurts conversion.

**Root cause**: `billPayorInfo` is set to `0` in the createBill payload.

**The flag's actual semantic** (often misread in initial scaffolds):

| Value | What it does |
|-------|--------------|
| `0` | **Blank form** — ToyyibPay shows empty Name/Email/Phone fields, ignores `billTo`/`billEmail`/`billPhone` for pre-fill, customer must re-type |
| `1` | **Pre-fill enabled** — ToyyibPay populates Name/Email/Phone from your `billTo`/`billEmail`/`billPhone` values, customer just confirms or edits |

**Common misread**: developers see `billPayorInfo` and read `0` as "no payer info needed" (skip the
form). It means the opposite — `0` shows the form blank, `1` shows it pre-filled.

**Fix**: always set `billPayorInfo => 1` AND ensure `billTo`/`billEmail`/`billPhone` are non-empty in
the payload. Validate server-side that customer email is required when the payment method is
ToyyibPay — it is not optional for online payments.

### Phone Format

ToyyibPay accepts the Malaysian `0123456789` format (leading zero, no `+60` prefix). Normalize
before sending:

```php
$phone = $validated['customer_phone'];
if (str_starts_with($phone, '+6')) {
    $phone = '0' . substr($phone, 2);  // +60123456789 -> 0123456789
}
```

Sending `+60123456789` MAY pre-fill correctly, but some downstream bank gateways reject the `+`
prefix during transaction processing. Stick with the `0` prefix.

### `getCategoryDetails` Response Key Casing (`CategoryName` vs `categoryName`)

**Symptom**: a "Test Connection" feature reports **valid** credentials as invalid or unexpected, even
though the same key works for real payments. The test call clearly reaches ToyyibPay and gets a real
category back — the code just fails to recognise it.

**Root cause**: `getCategoryDetails` returns the category name under the key **`CategoryName`**
(capital C), while its sibling keys are lowercase (`categoryDescription`, `categoryStatus`). JSON
keys are case-sensitive, so a parser that checks `categoryName` — matching the siblings' style —
silently misses the value and falls through to a generic failure.

```json
{"CategoryName":"YOUR CATEGORY NAME ","categoryDescription":"PAYMENT ","categoryStatus":"1"}
```

**The trap**: this endpoint is only ever listed in the API table as "test the connection" — its
response shape is undocumented, so first implementations *guess* the key and naturally guess the
consistent lowercase spelling. The guess is wrong.

**Why it hides**: the failure surfaces as a generic "invalid credentials" toast. If your frontend
never renders that toast layer, the message is invisible and the cause looks like a network or key
problem. Log the raw response body server-side so the capital-C key is visible regardless of the UI.

**Fix**: read the name under either casing — `$node['CategoryName'] ?? $node['categoryName']` — and
`trim()` it (ToyyibPay pads values with trailing spaces). See the Test Connection snippet above.

## Error Handling
- **Invalid category code**: verify `categoryCode` in the ToyyibPay dashboard
- **Amount validation**: must be in cents (integer), minimum `100` (RM 1.00)
- **Bill name too long**: max 30 characters — truncate before sending
- **API timeout**: use a 30s timeout with retry logic
- **Duplicate `billExternalReferenceNo`**: each order must have a unique reference
- **Fallback**: if bill creation fails, keep the order in `pending` and let the customer retry — never
  mark it paid on an unconfirmed response

## Rate Limits
- No official rate limit documented
- Recommended ceiling: ~10 requests/second
- Use a queue for bulk bill creation

## Testing
- **Sandbox URL**: https://dev.toyyibpay.com/
- **Production URL**: https://toyyibpay.com/
- **Test mode**: use sandbox credentials issued from the dashboard
- **Test banks**: the sandbox FPX page offers simulated banks with selectable success/failure outcomes
- Mock the HTTP layer in unit tests (e.g. Laravel's `Http::fake()`) so no live bills are created

## See Also
- `security/toyyibpay-webhook-verification` — hardened callback handling: API-side verification,
  idempotency, IP allowlist, audit checklist

Both items sketch a `ToyyibPayService`. If you install both, merge them into a single class — this
one contributes `createBill()`, `getBill()`, `isPaid()` and `testConnection()`; the security item
contributes `verifyCallback()` and masked credential logging.

## Projects Using This
- *(Add your projects here after implementing)*

---
*Documented: July 2026*
*Based on the ToyyibPay API reference plus production integration experience*
