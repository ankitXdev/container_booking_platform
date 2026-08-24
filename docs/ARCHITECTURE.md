# System Architecture

## 1. Three-Tier Architecture

The system uses three primary layers.

```text
┌──────────────────────────────┐
│      Presentation Layer      │
│          React UI            │
└──────────────┬───────────────┘
               │ REST / JSON
               ▼
┌──────────────────────────────┐
│       Application Layer      │
│        FastAPI Backend       │
│                              │
│ Auth | Providers | Containers│
│ Bookings | Payments | Admin  │
└──────────────┬───────────────┘
               │ SQLAlchemy
               ▼
┌──────────────────────────────┐
│          Data Layer          │
│          PostgreSQL          │
└──────────────────────────────┘
```

## 2. External Payment Service

Razorpay is integrated with the backend for payment processing.

```text
React
  |
  v
FastAPI
  |
  +---- create/prepare payment ----> Razorpay
  |
  <---- payment result -------------
  |
  +---- server-side verification
  |
  v
PostgreSQL
```

The backend should remain responsible for determining whether a booking is actually considered paid.

## 3. Backend Modules

### Authentication

Responsible for:
- Registration
- Login
- Password verification
- JWT creation
- Current-user identification

### Providers

Responsible for:
- Provider registration
- Provider profile
- Approval status
- Provider-specific authorization

### Containers

Responsible for:
- Container/capacity listings
- Availability
- Provider ownership
- Searchable container data

### Bookings

Responsible for:
- Booking creation
- Availability checks
- Booking status
- Cancellation rules
- Booking history

### Payments

Responsible for:
- Razorpay integration
- Payment records
- Payment verification
- Payment status

### Admin

Responsible for:
- Provider approval
- Monitoring
- Platform-level controls

## 4. Booking Consistency

A booking must not simply trust the availability returned by a previous search.

The correct flow is:

```text
Search
  ↓
Show available capacity
  ↓
Exporter selects capacity
  ↓
Create booking request
  ↓
Backend checks current availability
  ↓
Available?
 /     No      Yes
|        |
Reject   Reserve/continue
         ↓
      Payment
         ↓
      Confirm
```

The final availability check must happen on the backend.

## 5. Recommended Backend Structure

```text
backend/
└── app/
    ├── config/
    ├── controllers/
    ├── models/
    ├── routes/
    ├── schemas/
    ├── security/
    ├── services/
    ├── utils/
    └── main.py
```

This matches the layered organization already started in the current backend.
