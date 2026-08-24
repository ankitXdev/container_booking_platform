# User Flows

## Exporter

### Registration

```text
Open application
      ↓
Select Exporter
      ↓
Register
      ↓
Account created
      ↓
Login
```

### Search

```text
Exporter dashboard
      ↓
Enter shipment requirements
      ↓
Search
      ↓
Backend queries available capacity
      ↓
Results displayed
      ↓
Exporter selects listing
```

### Booking

```text
Select listing
      ↓
Enter required capacity
      ↓
Backend rechecks availability
      ↓
Available?
  /       No        Yes
|          |
Return     Create booking
error           ↓
            Payment
               ↓
        Razorpay verification
               ↓
        Confirm booking
```

## Provider

### Registration and Approval

```text
Register
   ↓
Provider details
   ↓
Pending
   ↓
Admin review
   ↓
Approved / Rejected
```

### Listing Capacity

```text
Approved provider
       ↓
Provider dashboard
       ↓
Add container listing
       ↓
Enter route/date/capacity/pricing
       ↓
Publish listing
       ↓
Exporter can search it
```

## Admin

```text
Admin login
    ↓
Dashboard
    |
    +--> Provider applications
    |       |
    |       +--> Approve
    |       +--> Reject
    |
    +--> Containers
    |
    +--> Bookings
    |
    +--> Payments
    |
    +--> Platform monitoring
```

## Sequence: Booking + Payment

```text
Exporter       FastAPI       PostgreSQL       Razorpay
   |              |               |               |
   |-- booking -->|               |               |
   |              |-- check ----->|               |
   |              |<-- available -|               |
   |              |                               |
   |              |-----------------------------> |
   |              |        create order           |
   |              |<----------------------------- |
   |              |                               |
   |<-------------| payment information           |
   |                                              |
   |---------------- payment -------------------->|
   |                                              |
   |              |<------- verification ---------|
   |              |               |               |
   |              |-- update ---->|               |
   |              |               |               |
   |<-- confirmed-|               |               |
```
