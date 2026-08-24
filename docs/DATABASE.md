# Database Design

PostgreSQL is the primary database.

The exact schema should evolve with the implementation, but the MVP requires the following core entities.

## Entity Overview

```text
Users
  |
  +---- Provider Profile
  |
  +---- Bookings
             |
             +---- Container
             |
             +---- Payment

Provider
  |
  +---- Containers
            |
            +---- Bookings
```

## 1. Users

Stores authentication and role information.

Suggested fields:

| Field | Purpose |
|---|---|
| user_id | Primary key |
| name | User name |
| email | Unique login email |
| password_hash | Hashed password |
| role | exporter/provider/admin |
| status | Account state |
| created_at | Creation timestamp |
| updated_at | Last update |

## 2. Providers

Stores provider-specific information.

Suggested fields:

| Field | Purpose |
|---|---|
| provider_id | Primary key |
| user_id | Owner user |
| business_name | Provider business |
| business_address | Business address |
| contact | Contact details |
| approval_status | pending/approved/rejected |
| created_at | Creation timestamp |

Relationship:

```text
users 1 ---- 0..1 providers
```

## 3. Containers

Represents available container capacity.

Suggested fields:

| Field | Purpose |
|---|---|
| container_id | Primary key |
| provider_id | Owning provider |
| container_type | Container type |
| origin | Shipping origin |
| destination | Shipping destination |
| departure_date | Planned departure |
| total_capacity | Total capacity |
| available_capacity | Remaining capacity |
| price | Pricing information |
| status | Listing status |

## 4. Bookings

Represents exporter reservations.

Suggested fields:

| Field | Purpose |
|---|---|
| booking_id | Primary key |
| exporter_id | Exporter |
| container_id | Selected capacity |
| booked_capacity | Capacity reserved |
| amount | Booking amount |
| status | Booking status |
| created_at | Booking creation time |

## 5. Payments

Stores payment information associated with bookings.

Suggested fields:

| Field | Purpose |
|---|---|
| payment_id | Primary key |
| booking_id | Related booking |
| razorpay_order_id | Razorpay order |
| razorpay_payment_id | Razorpay payment |
| amount | Paid amount |
| status | Payment status |
| created_at | Payment timestamp |

## Relationships

```text
users
 |
 +------ providers
 |
 +------ bookings ------ containers ------ providers
              |
              +------ payments
```

## Important Database Rule

When a booking is created, the system must ensure that:

```text
requested_capacity <= current_available_capacity
```

The availability update and booking creation should be handled safely so concurrent requests cannot overbook the same capacity.

## Migrations

Use Alembic once the schema stabilizes.

Recommended workflow:

```text
SQLAlchemy model change
        ↓
Alembic migration
        ↓
Review migration
        ↓
Run migration
        ↓
PostgreSQL updated
```
