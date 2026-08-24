# API Specification

This document describes the planned REST API surface. Exact request/response schemas should be finalized during implementation and kept synchronized with FastAPI's OpenAPI specification.

Base URL:

```text
http://127.0.0.1:8000
```

Swagger:

```text
/docs
```

ReDoc:

```text
/redoc
```

## Authentication

### POST `/auth/register`

Register a new account.

```json
{
  "name": "Example User",
  "email": "user@example.com",
  "password": "strong-password",
  "role": "exporter"
}
```

Roles:

```text
exporter
provider
admin
```

Admin creation should normally be controlled securely rather than allowing unrestricted public admin registration.

### POST `/auth/login`

Authenticate a user.

```json
{
  "email": "user@example.com",
  "password": "strong-password"
}
```

Response:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### Authentication Header

Protected routes use:

```text
Authorization: Bearer <jwt>
```

## Provider APIs

### POST `/providers`

Submit provider registration/profile information.

### GET `/providers/me`

Get the authenticated provider's profile.

### PATCH `/providers/me`

Update provider information.

### GET `/providers/{provider_id}`

Get provider information where permitted.

### GET `/admin/providers`

Admin endpoint for provider review.

### PATCH `/admin/providers/{provider_id}/approval`

Approve or reject a provider.

Example:

```json
{
  "status": "approved"
}
```

## Container APIs

### POST `/containers`

Create a container/capacity listing.

Provider authentication required.

Example:

```json
{
  "origin": "Mumbai",
  "destination": "Dubai",
  "departure_date": "2026-09-15",
  "available_capacity_kg": 500,
  "container_type": "20ft",
  "price_per_kg": 100
}
```

The exact fields should follow the final database/schema design.

### GET `/containers`

Search available container capacity.

Possible query parameters:

```text
origin
destination
departure_date
capacity
container_type
```

### GET `/containers/{container_id}`

Get container listing details.

### PATCH `/containers/{container_id}`

Update a provider's own container listing.

### DELETE `/containers/{container_id}`

Remove/deactivate a container listing where allowed.

## Booking APIs

### POST `/bookings`

Create a booking request.

### GET `/bookings`

Return bookings belonging to the authenticated user/provider according to role.

### GET `/bookings/{booking_id}`

Get booking details.

### PATCH `/bookings/{booking_id}/status`

Update booking status where the authenticated role has permission.

## Payment APIs

### POST `/payments/create-order`

Create a Razorpay payment order associated with a booking.

### POST `/payments/verify`

Verify Razorpay payment information on the backend.

### GET `/payments/{payment_id}`

Return payment information to authorized users.

## Admin APIs

### GET `/admin/users`

View users where permitted.

### GET `/admin/providers`

View provider applications.

### GET `/admin/containers`

Monitor container listings.

### GET `/admin/bookings`

Monitor bookings.

### GET `/admin/payments`

Monitor payment records.

## API Design Rules

- Use HTTP status codes consistently.
- Validate request bodies with Pydantic.
- Enforce authorization on every protected endpoint.
- Never trust role information supplied by the frontend.
- Never trust payment success information from the client alone.
- Validate ownership before modifying provider/container/booking resources.
