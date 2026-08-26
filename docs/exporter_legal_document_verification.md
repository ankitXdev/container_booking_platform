# Exporter Legal Document Verification

## Purpose

This document defines the documents an admin should verify before approving an exporter on the platform.

The purpose is to verify:

- Exporter identity
- Legal existence of the business
- Import/export authorization
- Business address
- Authorized representative
- Applicable export registrations and licences

---

## 1. Core Exporter Documents

| Document | Required? | What Admin Should Verify |
|---|---:|---|
| **PAN Card** | Required | Business/person identity and PAN details |
| **IEC (Import Export Code)** | **Required** | IEC number, exporter name, and consistency with business details |
| **GST Registration Certificate** | Required if GST-registered/applicable | GSTIN, legal name, and business details |
| **Business Registration Certificate** | Required for registered businesses | Legal existence and entity details |
| **Business Address Proof** | Required | Registered/business address |
| **Authorized Representative ID** | Required | Identity of the person operating the account |

---

## 2. Import Export Code (IEC)

The **IEC (Import Export Code)** is the most important exporter-specific document.

Admin should verify:

- IEC number is present.
- Exporter name matches the business/account information.
- Business/entity details are consistent with the application.
- IEC information appears valid/current.
- Any discrepancy between IEC and other business documents is reviewed before approval.

### Platform Rule

For an **Exporter business account**, the IEC should be treated as a mandatory document before the exporter can be approved.

```text
Exporter Application
        ↓
IEC Submitted
        ↓
Admin Verifies IEC
        ↓
Business Details Match?
        ↓
      Yes → Continue Approval
      No  → Reject / Request Correction
```

---

## 3. PAN Card

Admin should verify:

- PAN is readable.
- Name matches the exporter/business information.
- PAN details are consistent with other submitted documents.

---

## 4. GST Registration Certificate

Where GST registration is applicable, admin should verify:

- GSTIN is present.
- Legal/business name matches.
- Registered address is consistent.
- Details are consistent with the IEC and other documents.

GST should not be treated as universally mandatory for every possible exporter scenario where registration is not applicable.

---

## 5. Business Registration Certificate

Depending on the business structure, this may include:

- Certificate of Incorporation
- LLP registration documents
- Partnership registration documents
- Proprietorship registration documents
- Other applicable business registration documents

Admin should verify:

- Legal business name
- Registration number
- Entity type
- Registered details
- Consistency with the exporter application

---

## 6. Business Address Proof

Possible documents include:

- GST registration address
- Government/business registration address
- Utility bill
- Lease/rent agreement
- Property ownership document
- Other valid business address proof

Admin should verify:

- Address is readable.
- Address matches the exporter application.
- Any discrepancy is explained or supported by additional documentation.

---

## 7. Authorized Representative ID

Possible documents include:

- Aadhaar
- Passport
- Driving Licence
- Other accepted government-issued identification

Admin should verify:

- Representative's identity.
- Association with the exporter/business.
- Authorization to represent the business where required.

For companies and LLPs, an authorization letter or board resolution may be required where appropriate.

---

## 8. Conditional / Recommended Documents

These documents depend on the exporter's business and the goods/services being exported.

| Document | Requirement | Purpose |
|---|---|---|
| **Bank Account Proof** | Recommended | Confirms account/business-name consistency |
| **RCMC** | If applicable | Registration with the relevant Export Promotion Council |
| **Product-specific Licence** | If applicable | Authorization for regulated/restricted goods |
| **Product-specific Certificates** | If applicable | Compliance with destination/product requirements |
| **Other Government Permissions** | If applicable | Regulatory compliance for specific exports |
| **Insurance Certificate** | Recommended/if applicable | Cargo or business risk coverage |

---

## 9. Admin Verification Checklist

### Identity

- [ ] PAN has been submitted.
- [ ] Exporter/business name is consistent across documents.
- [ ] Authorized representative identity has been verified.

### Export Authorization

- [ ] IEC has been submitted.
- [ ] IEC details have been verified.
- [ ] IEC holder/exporter name matches the account/business details.
- [ ] Any discrepancy has been reviewed.

### Business Legitimacy

- [ ] Business registration document has been submitted where applicable.
- [ ] Registration number/details are present.
- [ ] GST certificate has been submitted where applicable.
- [ ] Business information is consistent across documents.

### Address

- [ ] Business address proof has been submitted.
- [ ] Address matches the exporter application.
- [ ] Address discrepancies have been resolved.

### Additional Export Requirements

- [ ] RCMC has been checked where applicable.
- [ ] Product-specific licences have been checked where applicable.
- [ ] Product-specific certificates have been checked where applicable.
- [ ] Other required government permissions have been checked.

### Document Quality

- [ ] Documents are readable.
- [ ] Documents are complete.
- [ ] Documents do not show obvious alteration or tampering.
- [ ] Expiry dates have been checked where applicable.
- [ ] Information is consistent across documents.

---

## 10. Document Status

Each uploaded document should have one of these statuses:

```text
PENDING
VERIFIED
REJECTED
```

### PENDING

The exporter has uploaded the document, but an admin has not completed verification.

### VERIFIED

The admin has reviewed and accepted the document.

### REJECTED

The document is invalid, incomplete, unreadable, inconsistent, or otherwise insufficient.

A rejection should include a reason.

Example:

```text
rejection_reason:
"IEC holder name does not match the exporter business name submitted in the application."
```

---

## 11. Exporter Approval Rule

An exporter should only be approved when:

1. All mandatory documents have been uploaded.
2. The IEC has been submitted and verified.
3. PAN and business details are consistent.
4. Required GST/business registration documents have been verified where applicable.
5. Business address has been verified.
6. Authorized representative has been verified.
7. Any applicable export-specific licences or registrations have been checked.
8. There are no unresolved document discrepancies.

### Recommended Approval Flow

```text
Exporter Registration
        ↓
Upload Documents
        ↓
Admin Document Review
        ↓
Verify IEC
        ↓
Verify Identity & Business
        ↓
Check Applicable Licences
        ↓
 ┌────────────────────┐
 │ All Requirements   │
 │ Satisfied?         │
 └─────────┬──────────┘
           │
      Yes  │  No
           │
           ↓
       APPROVE      REJECT / REQUEST
       EXPORTER     RE-UPLOAD
```

---

## 12. Suggested Database Structure

Use a separate `exporter_documents` table/collection.

```text
exporter_documents
-------------------
document_id
exporter_id
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
IEC
GST_CERTIFICATE
BUSINESS_REGISTRATION
ADDRESS_PROOF
AUTHORIZED_PERSON_ID
BANK_PROOF
RCMC
PRODUCT_LICENSE
PRODUCT_CERTIFICATE
OTHER
```

---

## 13. Recommended MVP Scope

For the initial version of the platform, use the following structure.

### Mandatory

1. PAN
2. **IEC**
3. GST Certificate — where applicable
4. Business Registration Certificate — where applicable
5. Business Address Proof
6. Authorized Representative ID

### Conditional

- Bank proof
- RCMC
- Product-specific licences
- Product-specific certificates
- Other government permissions
- Insurance

The **IEC should be the primary exporter-specific verification document**.

Sector-specific licences and certificates should remain conditional because their applicability depends on the exporter's business and the products being exported.

> **Note:** The exact legal and regulatory requirements can vary based on the exporter's business structure, goods, destination country, and applicable Indian regulations. The platform should therefore treat product-specific registrations and licences as conditional requirements and review them according to the exporter's declared activity.
