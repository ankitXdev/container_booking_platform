# Provider API Documentation — MVP Scope

## Overview

The Provider module manages logistics providers on the platform.

The MVP provider flow is:

```text
Provider Registration
        ↓
Pending Approval
        ↓
Admin Reviews Provider
        ↓
Approved / Rejected
        ↓
Approved Provider Can Participate
```

The API set below covers the provider functionality required for the MVP.

---

# 1. Provider APIs

## 1.1 Register Provider

### Endpoint

```http
POST /api/providers
```

### Purpose

Allows a logged-in user with the `provider` role to create their provider/business profile.

The provider is created with an initial approval status of:

```text
pending
```

The provider cannot be treated as an approved provider until an admin approves the profile.

### Request

```json
{
  "business_name": "ABC Logistics",
  "business_address": "Mumbai, Maharashtra",
  "contact": "9876543210"
}
```

### Authentication

Required.

The request must contain a valid JWT access token.

### Authorization

Only users with:

```text
role = provider
```

can register a provider profile.

### Main validations

- User must be authenticated.
- User must have the `provider` role.
- A user should not be able to create multiple provider profiles.
- Provider approval status starts as `pending`.

### Example response

```json
{
  "message": "Provider registration successful",
  "status": "pending"
}
```

---

# 2. Search / List Providers

## Endpoint

```http
GET /api/providers
```

### Purpose

Allows users to find providers available on the platform.

The API can support searching by business name.

### Example

```http
GET /api/providers?business_name=ABC
```

### Expected MVP behavior

Only **approved providers** should be visible to exporters when they search for providers.

Pending and rejected providers should not appear in the normal provider search.

### Example response

```json
[
  {
    "provider_id": 15,
    "business_name": "ABC Logistics",
    "business_address": "Mumbai, Maharashtra",
    "contact": "9876543210",
    "email": "abc@example.com"
  }
]
```

### Authentication

Required or public depending on the final application policy.

For the MVP, authenticated platform users are recommended.

### Important rule

The API should filter providers using:

```text
approval_status = approved
```

for normal user/exporter searches.

---

# 3. Get Provider Details

## Endpoint

```http
GET /api/providers/{id}
```

### Purpose

Returns the details of a specific provider.

This is useful when an exporter selects a provider from the provider search results.

### Example

```http
GET /api/providers/15
```

### Example response

```json
{
  "provider_id": 15,
  "business_name": "ABC Logistics",
  "business_address": "Mumbai, Maharashtra",
  "contact": "9876543210",
  "email": "abc@example.com",
  "approval_status": "approved"
}
```

### MVP rule

Normal users/exporters should only be able to view providers that are approved.

Admins may view providers regardless of their approval status.

---

# 4. Update Provider Profile

## Endpoint

```http
PUT /api/providers/{id}
```

### Purpose

Allows a provider to update their business information.

### Request

```json
{
  "business_name": "ABC Global Logistics",
  "business_address": "Mumbai, Maharashtra",
  "contact": "9999999999"
}
```

### Authentication

Required.

### Authorization

Only the provider who owns the profile should be allowed to update it.

An unrelated provider must not be able to modify another provider's profile.

### Example response

```json
{
  "message": "Provider profile updated successfully"
}
```

### MVP rule

Updating normal profile information should not automatically change the provider's approval status.

If the business-critical verification information changes, the system can require re-approval later.

---

# 5. Admin Provider APIs

Provider approval is an administrative operation.

These APIs must be protected with both:

```text
JWT authentication
+
admin role authorization
```

---

# 5.1 List Providers for Admin

## Endpoint

```http
GET /api/admin/providers
```

### Purpose

Allows an admin to see provider registrations and review their approval status.

### Optional filter

```http
GET /api/admin/providers?status=pending
```

### Example response

```json
[
  {
    "provider_id": 15,
    "business_name": "ABC Logistics",
    "business_address": "Mumbai, Maharashtra",
    "contact": "9876543210",
    "email": "abc@example.com",
    "approval_status": "pending"
  }
]
```

### Why this is needed

The admin dashboard needs a way to retrieve providers waiting for approval.

---

# 5.2 Approve Provider

## Endpoint

```http
PUT /api/admin/providers/{id}/approve
```

### Purpose

Allows an admin to approve a pending provider.

### Example

```http
PUT /api/admin/providers/15/approve
```

### State change

```text
pending
   ↓
approved
```

### Example response

```json
{
  "message": "Provider approved successfully",
  "status": "approved"
}
```

### Authorization

Admin only.

A provider or exporter must not be able to call this successfully.

---

# 5.3 Reject Provider

## Endpoint

```http
PUT /api/admin/providers/{id}/reject
```

### Purpose

Allows an admin to reject a provider registration.

### Example

```http
PUT /api/admin/providers/15/reject
```

### State change

```text
pending
   ↓
rejected
```

### Example response

```json
{
  "message": "Provider rejected successfully",
  "status": "rejected"
}
```

### Authorization

Admin only.

---

# 6. Provider Approval State

The MVP should use three basic provider states:

```text
pending
approved
rejected
```

## Pending

The provider has registered but has not yet been approved by an admin.

## Approved

The provider has been verified/accepted and can participate in the platform.

## Rejected

The admin has rejected the provider registration.

### State flow

```text
              ┌───────────┐
              │  PENDING  │
              └─────┬─────┘
                    /                    /                     ↓     ↓
        ┌────────────┐ ┌────────────┐
        │  APPROVED  │ │  REJECTED  │
        └────────────┘ └────────────┘
```

---

# 7. Complete Provider API List for MVP

| Method | Endpoint | User | Function |
|---|---|---|---|
| POST | `/api/providers` | Provider | Register provider |
| GET | `/api/providers` | User/Exporter | Search approved providers |
| GET | `/api/providers/{id}` | User/Exporter | View provider details |
| PUT | `/api/providers/{id}` | Provider owner | Update provider profile |
| GET | `/api/admin/providers` | Admin | View/manage provider registrations |
| PUT | `/api/admin/providers/{id}/approve` | Admin | Approve provider |
| PUT | `/api/admin/providers/{id}/reject` | Admin | Reject provider |

---

# 8. APIs Currently Missing

Based on the current provider implementation, the following should be added for a complete MVP:

```text
GET  /api/providers/{id}
PUT  /api/providers/{id}

GET  /api/admin/providers
PUT  /api/admin/providers/{id}/approve
PUT  /api/admin/providers/{id}/reject
```

The existing provider search should also be updated so normal users see only approved providers.

---

# 9. What Is NOT Required in the Provider Module

The following should be handled by other modules rather than being added to the basic Provider API:

- Container creation
- Available capacity listing
- Container booking
- Booking approval
- Payment processing
- Shipment tracking
- Notifications
- Reviews/ratings

These belong to later modules in the overall MVP architecture.

The important provider responsibility is:

```text
Create Profile
      ↓
Wait for Admin Approval
      ↓
Become Approved Provider
      ↓
Manage Provider Profile
      ↓
Create/List Available Capacity
```

---

# 10. Recommended MVP Flow

```text
                    PROVIDER
                       │
                       │ POST /api/providers
                       ▼
              ┌─────────────────┐
              │ Provider Created│
              │    PENDING      │
              └────────┬────────┘
                       │
                       ▼
                     ADMIN
                       │
              GET /api/admin/providers
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
     PUT .../approve     PUT .../reject
              │                 │
              ▼                 ▼
          APPROVED           REJECTED
              │
              ▼
       Provider can use
       platform features
```

---

# 11. Important Security Rules

Every provider-related API should enforce appropriate authorization.

### Provider APIs

A provider can:

- Create their own profile.
- View allowed provider information.
- Update their own profile.

A provider cannot:

- Approve another provider.
- Reject another provider.
- Modify another provider's profile.

### Admin APIs

An admin can:

- View all provider registrations.
- Approve providers.
- Reject providers.

### Exporter/User APIs

An exporter should:

- Search approved providers.
- View approved provider details.

An exporter should not:

- Approve/reject providers.
- Modify provider profiles.
- Access private admin information.

---

# 12. Provider Module MVP Summary

The Provider module's main job is to establish a trusted logistics provider on the platform.

The core workflow is:

```text
REGISTER
   ↓
PENDING
   ↓
ADMIN REVIEW
   ↓
APPROVED / REJECTED
   ↓
APPROVED PROVIDER
   ↓
PROVIDER PARTICIPATES IN PLATFORM
```

This is sufficient for the Provider management portion of the MVP. The next major module after provider approval should handle the provider's **container/capacity listings**, because that is what exporters will actually search and book.
