# Security Headers
*Production-grade HTTP security headers with Content Security Policy for web applications*

## Threat Model
- **Threat**: XSS attacks, clickjacking, MIME sniffing, man-in-the-middle attacks, code injection
- **Impact**: Data theft, session hijacking, malicious code injection, unauthorized framing
- **Severity**: High

## Use Case
- All web applications in production
- APIs that serve web clients
- Applications handling sensitive data (payments, user info)
- Compliance requirements (PCI-DSS, OWASP Top 10)

## Headers Reference

| Header | Recommended Value | Purpose |
|--------|-------------------|---------|
| **Strict-Transport-Security** | `max-age=31536000; includeSubDomains` | Force HTTPS, prevent SSL stripping |
| **Content-Security-Policy** | See CSP section below | Prevent XSS, control resource loading |
| **X-Frame-Options** | `SAMEORIGIN` | Prevent clickjacking |
| **X-Content-Type-Options** | `nosniff` | Prevent MIME sniffing attacks |
| **Referrer-Policy** | `strict-origin-when-cross-origin` | Control referrer information leakage |
| **Permissions-Policy** | `geolocation=(), microphone=(), camera=()` | Disable unnecessary browser features |

## CSP Directives Explained

```
default-src 'self'           → Only load resources from same origin
script-src 'self' cdn...     → Allow scripts from self and trusted CDNs
style-src 'self' 'unsafe-inline' → Allow inline styles (needed for many CSS frameworks)
font-src 'self' fonts...     → Allow fonts from self and font providers
img-src 'self' data: blob:   → Allow images, data URIs, blobs
connect-src 'self'           → XHR/fetch only to same origin + API domains
frame-ancestors 'self'       → Only allow framing by same origin
form-action 'self'           → Forms can only submit to self + trusted domains
base-uri 'self'              → Prevent base tag injection
object-src 'none'            → Block plugins (Flash, Java)
```

## Implementation

### PHP / Laravel

```php
<?php
// app/Http/Middleware/SecurityHeaders.php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class SecurityHeaders
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);

        // Skip in local development for easier debugging
        if (app()->environment('local')) {
            return $response;
        }

        $response->headers->set(
            'Strict-Transport-Security',
            'max-age=31536000; includeSubDomains'
        );

        $response->headers->set('Content-Security-Policy', $this->buildCsp());

        $response->headers->set('X-Frame-Options', 'SAMEORIGIN');
        $response->headers->set('X-Content-Type-Options', 'nosniff');
        $response->headers->set('Referrer-Policy', 'strict-origin-when-cross-origin');
        $response->headers->set(
            'Permissions-Policy',
            'geolocation=(), microphone=(), camera=(), payment=(), usb=()'
        );

        return $response;
    }

    private function buildCsp(): string
    {
        return implode('; ', [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com",
            "img-src 'self' data: blob:",
            "connect-src 'self'",
            "frame-ancestors 'self'",
            "form-action 'self'",
            "base-uri 'self'",
            "object-src 'none'",
        ]);
    }
}
```

**Registration (Laravel 11+):**
```php
// bootstrap/app.php
use App\Http\Middleware\SecurityHeaders;

return Application::configure(basePath: dirname(__DIR__))
    ->withMiddleware(function (Middleware $middleware) {
        $middleware->append(SecurityHeaders::class);
    })
    ->create();
```

**Registration (Laravel 10 and earlier):**
```php
// app/Http/Kernel.php
protected $middleware = [
    \App\Http\Middleware\SecurityHeaders::class,
];
```

### Node.js / Express

```javascript
// middleware/securityHeaders.js

function securityHeaders(req, res, next) {
    // Skip in development
    if (process.env.NODE_ENV === 'development') {
        return next();
    }

    res.setHeader(
        'Strict-Transport-Security',
        'max-age=31536000; includeSubDomains'
    );

    const csp = [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net",
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
        "font-src 'self' https://fonts.gstatic.com",
        "img-src 'self' data: blob:",
        "connect-src 'self'",
        "frame-ancestors 'self'",
        "form-action 'self'",
        "base-uri 'self'",
        "object-src 'none'",
    ].join('; ');

    res.setHeader('Content-Security-Policy', csp);
    res.setHeader('X-Frame-Options', 'SAMEORIGIN');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
    res.setHeader(
        'Permissions-Policy',
        'geolocation=(), microphone=(), camera=(), payment=(), usb=()'
    );

    next();
}

// Usage: app.use(securityHeaders);
module.exports = securityHeaders;
```

### Java / Spring Boot

```java
// config/SecurityHeadersConfig.java

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityHeadersConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.headers(headers -> headers
            .httpStrictTransportSecurity(hsts -> hsts
                .includeSubDomains(true)
                .maxAgeInSeconds(31536000)
            )
            .contentSecurityPolicy(csp -> csp
                .policyDirectives(buildCsp())
            )
            .frameOptions(frame -> frame.sameOrigin())
            .contentTypeOptions(content -> {})
            .referrerPolicy(referrer -> referrer
                .policy(ReferrerPolicyHeaderWriter.ReferrerPolicy
                    .STRICT_ORIGIN_WHEN_CROSS_ORIGIN)
            )
            .permissionsPolicy(permissions -> permissions
                .policy("geolocation=(), microphone=(), camera=(), payment=(), usb=()")
            )
        );

        return http.build();
    }

    private String buildCsp() {
        return String.join("; ",
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com",
            "img-src 'self' data: blob:",
            "connect-src 'self'",
            "frame-ancestors 'self'",
            "form-action 'self'",
            "base-uri 'self'",
            "object-src 'none'"
        );
    }
}
```

### Nginx (Any Backend)

```nginx
# /etc/nginx/conf.d/security-headers.conf
# Include in your server block: include conf.d/security-headers.conf;

add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: blob:; connect-src 'self'; frame-ancestors 'self'; form-action 'self'; base-uri 'self'; object-src 'none'" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=(), usb=()" always;
```

### Apache (Any Backend)

```apache
# .htaccess or httpd.conf
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: blob:; connect-src 'self'; frame-ancestors 'self'; form-action 'self'; base-uri 'self'; object-src 'none'"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=(), usb=()"
```

## Configuration

### Customizing CSP Directives

Adapt the CSP directives to your project's needs:

```
# Add your CDN domains to script-src and style-src
script-src 'self' https://your-cdn.com

# Add your image storage to img-src
img-src 'self' data: blob: https://your-storage.com

# Add your API domain to connect-src
connect-src 'self' https://api.yourdomain.com

# Add payment gateways to form-action
form-action 'self' https://your-payment-gateway.com
```

### Environment-Based Toggle

All implementations above skip headers in development mode. In production, ensure your environment is set correctly:

```
# .env
APP_ENV=production        # Laravel
NODE_ENV=production       # Node.js
SPRING_PROFILES_ACTIVE=prod  # Spring Boot
```

## Validation Rules
- All 6 headers must be present in every production response
- CSP must not use `'unsafe-eval'` unless absolutely required (e.g., Vue.js dev mode)
- HSTS `max-age` must be at least 31536000 (1 year)
- Headers should NOT be applied in local development (for debugging ease)

## Error Responses
- **CSP violation**: Browser blocks the resource and logs to console
- **Frame violation**: Page refuses to render in iframe (X-Frame-Options)
- **Mixed content**: Browser blocks HTTP resources on HTTPS page (HSTS)

## Testing

### Security Scanner Tools
- securityheaders.com — Online header checker (aim for A+ grade)
- Mozilla Observatory (observatory.mozilla.org) — Comprehensive security scan
- Qualys SSL Labs (ssllabs.com/ssltest/) — SSL/TLS analysis

### Manual Verification
```bash
# Check all headers with curl
curl -I https://yourdomain.com

# Expected output includes:
# strict-transport-security: max-age=31536000; includeSubDomains
# content-security-policy: default-src 'self'; ...
# x-frame-options: SAMEORIGIN
# x-content-type-options: nosniff
# referrer-policy: strict-origin-when-cross-origin
# permissions-policy: geolocation=(), microphone=(), camera=()
```

### Security Audit Checklist
- [ ] All 6 headers present in production responses
- [ ] HSTS max-age is at least 31536000 (1 year)
- [ ] CSP doesn't use `'unsafe-inline'` for scripts (if possible)
- [ ] CSP doesn't use `'unsafe-eval'` (if possible)
- [ ] X-Frame-Options is SAMEORIGIN or DENY
- [ ] Headers NOT applied in local/development environment
- [ ] All external resource domains listed in appropriate CSP directives
- [ ] Payment gateway domains in form-action CSP (if applicable)

## Common CSP Issues

| Issue | Solution |
|-------|----------|
| Inline scripts blocked | Add `'unsafe-inline'` to script-src or use nonces |
| CDN resources blocked | Add CDN domain to the appropriate directive |
| Images not loading | Add image source domain to `img-src` |
| API calls failing | Add API domain to `connect-src` |
| Payment redirect blocked | Add payment gateway domain to `form-action` |
| Fonts not loading | Add font provider to `font-src` |
| WebSocket blocked | Add `wss://` domain to `connect-src` |

## Gradual Deployment

Start with report-only mode to find violations without breaking your site:

1. Deploy with `Content-Security-Policy-Report-Only` header instead of `Content-Security-Policy`
2. Set up a report endpoint to collect violations
3. Monitor violations for 1-2 weeks
4. Adjust directives based on legitimate resources being blocked
5. Switch to enforcing mode (`Content-Security-Policy`)

```
# Report-only header (does not block, only reports)
Content-Security-Policy-Report-Only: default-src 'self'; ... ; report-uri /csp-report
```

## Logging & Monitoring
- Log all CSP violations (report-uri or report-to)
- Alert on sudden spike in CSP violations (may indicate attack or broken deployment)
- Monitor security header grades on securityheaders.com periodically
- Review CSP directives when adding new third-party services

## Projects Using This
- *(Add your projects here after implementing)*

---
*Documented: March 2026*
*Based on OWASP Security Headers recommendations*
