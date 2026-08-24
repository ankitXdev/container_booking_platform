# Security

## Authentication

JWT is used for API authentication.

A protected request should contain:

```text
Authorization: Bearer <token>
```

## Password Security

Passwords must be hashed before being stored.

The database must never contain plaintext passwords.

## Role-Based Authorization

Role checks must happen on the backend.

Example:

```text
Exporter → booking operations
Provider → own container operations
Admin → platform operations
```

The frontend may hide UI elements, but hiding a button is not authorization.

## Provider Approval

Provider status must be checked before allowing provider-only operations.

```text
pending → blocked
approved → allowed
rejected → blocked
```

## JWT Secrets

JWT secrets must come from environment/secure secret management.

Do not hard-code secrets in Python source.

## Database Credentials

Database credentials must remain outside source control.

## Razorpay Security

The Razorpay secret must only exist on the backend.

The client should not be trusted to declare that a payment succeeded.

The backend should verify the payment signature/result and update the payment/booking state accordingly.

## Booking Security

The backend must check:

1. User is authenticated.
2. User has permission to create the booking.
3. Container exists.
4. Container is active.
5. Provider is approved.
6. Requested capacity is available.
7. Booking amount is calculated/validated server-side.
8. Payment is verified before final confirmation.

## Production Requirements

Before deployment:

- HTTPS
- Secure cookies/tokens where appropriate
- CORS restrictions
- Rate limiting
- Secure secret management
- Database backups
- Logging
- Monitoring
- Dependency updates
- Automated security testing
