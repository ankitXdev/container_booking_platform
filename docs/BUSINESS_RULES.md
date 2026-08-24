# Business Rules

## BR-01 Roles

Every account has a role:

```text
exporter
provider
admin
```

The backend, not the frontend, determines whether an operation is authorized.

## BR-02 Provider Approval

A provider begins with:

```text
approval_status = pending
```

A provider cannot use provider marketplace functionality until approved.

Possible states:

```text
pending
approved
rejected
```

## BR-03 Container Ownership

A provider may only create, update, or remove its own container listings.

## BR-04 Search Does Not Reserve Capacity

Searching for a container does not reserve space.

Availability must be checked again when a booking is submitted.

## BR-05 No Overbooking

A booking cannot reserve more capacity than is currently available.

```text
requested_capacity <= available_capacity
```

## BR-06 Booking and Payment

A payment should be associated with a specific booking.

The booking should not be marked as successfully paid solely because the frontend reports payment success.

The backend must verify the payment with Razorpay.

## BR-07 Payment Failure

A failed payment must not result in a confirmed paid booking.

## BR-08 Authorization

Exporters cannot modify provider-owned container listings.

Providers cannot modify another provider's listings.

Normal users cannot perform admin operations.

## BR-09 Booking Visibility

Exporters can view their own bookings.

Providers can view bookings associated with their containers.

Admins can monitor platform bookings.

## BR-10 Provider Rejection

A rejected provider should not be able to operate as an approved provider unless the platform defines a re-application/review process.

## BR-11 Capacity

Available capacity must never become negative.

## BR-12 State Transitions

Suggested booking states:

```text
pending
payment_pending
confirmed
cancelled
completed
failed
```

Suggested payment states:

```text
created
pending
paid
failed
refunded
```

These states should be finalized before implementation.

## BR-13 Admin Authority

Admin operations are platform-level operations and require explicit admin authorization.

## BR-14 Transaction Safety

Booking, payment state, and capacity updates should use appropriate database transactions.

## BR-15 Sensitive Data

Passwords, JWT secrets, database credentials, and payment secrets must never be committed to source control.
