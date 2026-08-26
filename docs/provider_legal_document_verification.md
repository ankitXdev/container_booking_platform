# Provider Legal Document Verification

## Purpose

This document defines the legal and business documents an admin should verify before approving a provider on the platform.

The goal is to verify:

- Provider identity
- Legal existence of the business
- Business address
- Authority of the person registering the business
- Relevant licences and permits
- Supporting financial and operational information

---

## 1. Mandatory Documents

These documents should be required for the initial provider approval process.

| Document | What Admin Should Verify | Priority |
|---|---|---|
| **PAN Card** | Legal identity and PAN details of the provider/business | Required |
| **GST Registration Certificate** | GST registration, legal business name, GSTIN, and consistency with submitted details | Required |
| **Business Registration Certificate** | Legal existence of the company, LLP, partnership, proprietorship, or other registered entity, where applicable | Required |
| **Business Address Proof** | Provider's submitted business address and consistency with official records | Required |
| **Authorized Representative ID** | Identity of the person registering/representing the business | Required |

### 1.1 PAN Card

Admin should verify:

- PAN is clearly visible and readable.
- Name matches the provider's submitted legal/business information.
- PAN details are consistent with other submitted documents.

### 1.2 GST Registration Certificate

Admin should verify:

- GSTIN is present.
- Legal business name matches the provider's submitted information.
- Registered address is consistent with the submitted business address.
- Registration details appear valid/current.

### 1.3 Business Registration Certificate

Depending on the business structure, this may include:

- Certificate of Incorporation
- LLP Registration/Certificate
- Partnership registration documents
- Proprietorship registration documents
- Other applicable business registration documents

Admin should verify:

- Legal business name
- Registration number
- Business/entity type
- Registered details
- Consistency with the provider's application

### 1.4 Business Address Proof

Possible documents include:

- GST registration address
- Registered office document
- Utility bill
- Lease/rent agreement
- Property ownership document
- Other valid government/business address proof

Admin should verify:

- Address is readable.
- Address matches the provider application.
- Any difference between documents is explained or supported by additional evidence.

### 1.5 Authorized Representative ID

Possible IDs include:

- Aadhaar
- Passport
- Driving Licence
- Other accepted government-issued identification

Admin should verify:

- Name and identity of the representative.
- Relationship/association with the business.
- Authorization to represent the business where required.

For companies and LLPs, an authorization letter or board resolution may be required where appropriate.

---

## 2. Conditional / Recommended Documents

These documents should be required only when applicable to the provider or service being offered.

| Document | Purpose | Requirement |
|---|---|---|
| **Bank Account Proof** | Confirms payment account belongs to the provider/business | Recommended |
| **Trade / Shop & Establishment Licence** | Confirms applicable local business authorization | If applicable |
| **Transport Permit / Licence** | Confirms authorization for relevant transport operations | If applicable |
| **Insurance Certificate** | Confirms applicable business, vehicle, cargo, or liability insurance | If applicable |
| **Company Authorization Letter / Board Resolution** | Confirms representative has authority to act for the company | If applicable |
| **Warehouse / Office Proof** | Supports verification of physical operating premises | Recommended |
| **Other Regulatory Licence** | Covers sector-specific legal requirements | If applicable |

---

## 3. Admin Verification Checklist

Before approving a provider, the admin should check:

### Identity

- [ ] Provider/business name is consistent across documents.
- [ ] PAN details are valid and readable.
- [ ] Authorized representative's identity has been verified.

### Business Legitimacy

- [ ] Business registration document has been provided where applicable.
- [ ] Registration number/details are present.
- [ ] GST certificate has been provided where applicable.
- [ ] GST/business details are consistent with the application.

### Address

- [ ] Business address proof has been provided.
- [ ] Address matches the submitted provider information.
- [ ] Any discrepancy has been reviewed and resolved.

### Authorization

- [ ] Person submitting the application is associated with the business.
- [ ] Authorization document has been provided where required.
- [ ] Company/LLP representative has appropriate authority where applicable.

### Additional Regulatory Requirements

- [ ] Applicable trade licence has been checked.
- [ ] Applicable transport permits/licences have been checked.
- [ ] Applicable insurance has been checked.
- [ ] Any other sector-specific requirement has been checked.

### Document Quality

- [ ] Documents are readable.
- [ ] Documents are complete.
- [ ] Documents do not show obvious alteration or tampering.
- [ ] Expiry dates have been checked where applicable.
- [ ] Information is consistent across documents.

---

## 4. Document Status

Each uploaded document should have one of the following statuses:

```text
PENDING
VERIFIED
REJECTED
```

### PENDING

The document has been uploaded but has not yet been reviewed by an admin.

### VERIFIED

The admin has reviewed the document and accepted it.

### REJECTED

The document is invalid, incomplete, unreadable, inconsistent, or otherwise insufficient.

A rejection should include a reason.

Example:

```text
rejection_reason:
"GST certificate address does not match the business address submitted in the provider application."
```

---

## 5. Provider Approval Rule

A provider should only be approved when:

1. All mandatory documents have been uploaded.
2. All mandatory documents have been verified.
3. The provider's identity and business details are consistent.
4. Any applicable licences or permits have been verified.
5. There are no unresolved document discrepancies.

Example approval flow:

```text
Provider Registration
        ↓
Upload Required Documents
        ↓
Admin Document Review
        ↓
 ┌───────────────┐
 │ All Required  │
 │ Documents OK? │
 └───────┬───────┘
         │
    Yes  │  No
         │
         ↓
      Approve       ← Reject / Request Re-upload
      Provider
```

---

## 6. Suggested Database Structure

A separate `provider_documents` table/collection should be used instead of storing all document information directly in the provider table.

```text
provider_documents
------------------
document_id
provider_id
document_type
document_url
document_number
status
rejection_reason
uploaded_at
verified_at
verified_by
```

### Document Types

```text
PAN
GST_CERTIFICATE
BUSINESS_REGISTRATION
ADDRESS_PROOF
AUTHORIZED_PERSON_ID
BANK_PROOF
TRADE_LICENSE
TRANSPORT_PERMIT
INSURANCE
OTHER
```

---

## 7. Recommended MVP Scope

For the initial version of the platform, keep the mandatory verification process simple.

### Mandatory

1. PAN
2. GST Certificate
3. Business Registration Certificate
4. Business Address Proof
5. Authorized Representative ID

### Conditional

- Bank proof
- Trade licence
- Transport permit
- Insurance
- Authorization letter / board resolution
- Other applicable licences

Sector-specific documents should be made conditional rather than requiring every provider to submit every possible licence.

> **Note:** The exact legal documents and licences required can vary depending on the provider's business structure, location, and the specific logistics/transport services they provide. The platform should therefore treat sector-specific permits as conditional requirements rather than universal requirements.
