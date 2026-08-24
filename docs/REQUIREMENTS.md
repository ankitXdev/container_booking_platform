# Software Requirements Specification

## 1. Product Overview

The Container Space Marketplace is a three-sided marketplace connecting exporters, logistics providers, and administrators.

The central problem is that small exporters may have cargo quantities too small to justify an entire container. The platform provides a centralized way to discover and book available container capacity.

## 2. Actors

### Exporter

Uses the platform to find and book available container space.

### Provider

Supplies container capacity and manages its availability.

### Admin

Controls provider approval and monitors the marketplace.

## 3. Functional Requirements

### FR-01 User Registration

The system shall allow users to create accounts.

### FR-02 Authentication

The system shall authenticate users using email/password credentials and issue JWT access tokens.

### FR-03 Role-Based Authorization

The system shall restrict operations according to exporter, provider, and admin roles.

### FR-04 Provider Registration

A user shall be able to register as a logistics provider and submit provider information.

### FR-05 Provider Approval

Administrators shall be able to approve or reject provider applications.

### FR-06 Container Listing

Approved providers shall be able to list available container capacity.

### FR-07 Availability Management

Providers shall be able to update the availability of their listed capacity.

### FR-08 Container Search

Exporters shall be able to search available container capacity.

### FR-09 Filtering

The system shall support relevant filters defined by the product design, such as route/date/capacity where applicable.

### FR-10 Booking

Exporters shall be able to create bookings against available capacity.

### FR-11 Availability Validation

The system shall validate availability at booking time to reduce overbooking.

### FR-12 Booking Management

Users shall be able to view relevant booking information and status.

### FR-13 Payment

The system shall integrate Razorpay for online payment.

### FR-14 Payment Verification

The backend shall verify payment results before marking the corresponding booking as paid/confirmed.

### FR-15 Administration

Administrators shall be able to monitor providers, containers, bookings, and payment-related information within the MVP scope.

## 4. Non-Functional Requirements

### Security

- Passwords must be hashed.
- Authentication must use secure tokens.
- Secrets must not be committed to source control.
- Role authorization must be enforced server-side.

### Reliability

Booking operations should maintain database consistency.

### Performance

Container searches should return results quickly enough for normal interactive use.

### Scalability

The backend should be structured so that additional providers, exporters, containers, and bookings can be added without changing the overall architecture.

### Maintainability

The codebase should maintain separation between routes, business logic, database models, schemas, and security.

### Usability

The frontend should provide clear workflows for each role.

## 5. MVP Boundary

The MVP focuses on:

```text
Authentication
      +
Provider approval
      +
Container discovery
      +
Booking
      +
Payment
      +
Basic administration
```

Advanced logistics and analytics features are outside the MVP.
