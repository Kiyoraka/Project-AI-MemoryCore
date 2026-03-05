# 🔒 Security Entry Format
*Template for security pattern entries*

## Required Fields
- Pattern name and description
- Threat it addresses
- Implementation
- Testing/verification
- Projects using this

## Template

```markdown
# [Security Pattern Name]
*[What security concern this addresses]*

## Threat Model
- **Threat**: [What attack/risk this prevents]
- **Impact**: [What could happen without this]
- **Severity**: [High/Medium/Low]

## Use Case
- When to implement this
- Systems that need this
- Compliance requirements (if any)

## Implementation

### Backend
```php
// Security implementation code
```

### Middleware (if applicable)
```php
// Middleware for enforcement
```

### Frontend (if applicable)
```javascript
// Frontend security measures
```

### Database (if applicable)
```sql
-- Security-related schema
```

## Configuration

### Environment Variables
```env
# Security-related config
```

### Config Files
```php
// Security configuration
```

## Validation Rules
- [Rule 1]: [How to validate]
- [Rule 2]: [How to validate]

## Error Responses
- [Scenario 1]: [Response code, message]
- [Scenario 2]: [Response code, message]

## Testing

### Test Cases
- [Test 1]: [What to verify]
- [Test 2]: [What to verify]

### Security Audit Checklist
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]

## Logging & Monitoring
- What to log
- Alert conditions
- Audit trail requirements

## Projects Using This
- [Project 1]
- [Project 2]

---
*Documented: [Date]*
```

## Example Entry Names
- `role-based-access` - RBAC implementation
- `api-authentication` - API auth (Sanctum/JWT)
- `input-validation` - Input sanitization
- `csrf-protection` - CSRF token handling
- `rate-limiting` - Request rate limits
- `password-policy` - Password requirements

---
*Format v1.0 - January 3, 2026*
