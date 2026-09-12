# Version 2.0 (v2.0) Product & Technical Roadmap
## Cargo Space Booking Platform — Digital Freight Forwarding & Logistics Network

---

## Executive Summary

The **Version 1.0 (MVP)** established the core three-sided marketplace foundation:
- Role-based authentication & permissions (Exporter, Provider, Admin)
- KYC compliance & document verification (IEC, GST, MTO License)
- Container discovery with capacity visualizer bars and route timelines
- Booking reservation and dynamic tariff calculation
- Razorpay payment gateway integration
- Provider fleet management and public track record profiles
- Administrator verification console

**Version 2.0 (v2.0)** transitions the platform from a regional container capacity marketplace into a **production-grade digital freight forwarding ecosystem**. It introduces real-time IoT/AIS vessel tracking, multimodal logistics, dynamic spot-bidding, automated digital shipping documentation (e-BL), escrow milestone payments, in-app communication, and 3D cargo load optimization.

---

## Core Pillars of Version 2.0

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                           VERSION 2.0 ARCHITECTURE                       │
├───────────────────┬───────────────────┬─────────────────────────────────┤
│  TRACK & TRACE    │  COMMERCE & TRUST │  DIGITAL DOCUMENTATION & TOOLS  │
├───────────────────┼───────────────────┼─────────────────────────────────┤
│ • AIS Vessel GPS  │ • Escrow Payments │ • Automated Bill of Lading      │
│ • Milestone Engine│ • Spot Bidding    │ • 3D Cargo Load Optimization    │
│ • Live Map Radar  │ • Provider SLAs   │ • Digital Customs Clearance     │
│ • Port Congestion │ • Multi-Currency  │ • In-App Messaging & WhatsApp   │
└───────────────────┴───────────────────┴─────────────────────────────────┘
```

---

## 1. Live Vessel & Container Tracking (AIS / IoT)

### The Problem in MVP
Exporters see the scheduled `departure_date`, but have zero visibility into where the vessel or cargo is after departure.

### Version 2.0 Capabilities
- **AIS GPS Vessel Tracking**: Integrate with marine data APIs (e.g., MarineTraffic, AISHub, or FleetMon) to plot vessel locations in real time.
- **Interactive Maritime Map**: Leaflet / Mapbox dashboard showing:
  - Current vessel coordinates and nautical speed (knots).
  - Historical route trail and predicted path.
  - Port congestion heatmaps and weather warning overlays.
- **Milestone Progress Tracker**:
  ```text
  [1. Cargo Received] ➔ [2. Customs Cleared] ➔ [3. Loaded on Vessel] ➔ [4. In Transit (Sea)] ➔ [5. Arrived at Destination Port] ➔ [6. Gate Out / Delivered]
  ```
- **Automated Delay Alerts**: Push notifications and SMS when ETA slips by more than 12 hours due to weather or port delays.

---

## 2. Multi-Leg & Intermodal Logistics

### The Problem in MVP
Listings are strictly single-leg port-to-port ocean voyages (e.g., Mumbai JNPT to Dubai).

### Version 2.0 Capabilities
- **Inland Container Depot (ICD) Integration**: Support originating from dry ports and inland hubs (e.g., ICD Tughlakabad, ICD Ludhiana) with combined Rail + Sea routing.
- **Last-Mile Drayage & Trucking**: Add optional origin pick-up and destination delivery checkboxes to the booking flow.
- **Transshipment Hubs Support**: Bookings that involve feeder vessels connecting through hub ports (e.g., Colombo, Singapore, Salalah) with automatic layover time estimations.

---

## 3. Dynamic Pricing & Spot Market Bidding

### The Problem in MVP
Prices are static per-kg tariffs set by the provider.

### Version 2.0 Capabilities
- **Spot Market / Space Auction (48h Clearance)**:
  - If a container has >20% unsold space 48 to 72 hours before departure, providers can enable "Spot Bidding".
  - Exporters can place binding bids for surplus weight below base tariff.
  - Provider can accept or counter-offer, maximizing vessel utilization.
- **Automated Surcharge Calculator**:
  - Bunker Adjustment Factor (BAF) tied to real-time marine fuel index.
  - Terminal Handling Charges (THC) and Currency Adjustment Factor (CAF) itemized transparently.

---

## 4. Digital Freight Documents & e-BL (Bill of Lading)

### The Problem in MVP
Document verification only validates static onboarding KYC (IEC, GST). Voyage-specific shipping documents are offline.

### Version 2.0 Capabilities
- **Automated Bill of Lading (e-BL)**:
  - Generates verifiable PDF e-BL upon vessel departure with SHA-256 cryptographic verification seal and QR code.
- **Export Documentation Vault per Booking**:
  - Exporters upload: Commercial Invoice, Packing List, Certificate of Origin, Shipping Bill.
  - Providers upload: Sea Waybill / Mate's Receipt, Container Seal Number, Inspection Certificate.
- **Customs Broker Integration**:
  - Role-based portal for CHA (Customs House Agents) to sign off on export clearings.

---

## 5. Escrow Payments & Milestone Payouts

### The Problem in MVP
100% of the payment is collected upfront via Razorpay and held in the platform account with manual reconciliation.

### Version 2.0 Capabilities
- **B2B Escrow Smart Payouts**:
  - **Phase 1 (Booking)**: 30% deposit held in escrow to reserve slot.
  - **Phase 2 (Departure)**: 50% released to provider upon e-BL issuance and vessel gate-in.
  - **Phase 3 (Delivery)**: Remaining 20% released upon arrival at destination port.
- **Multi-Currency Settlement**:
  - Exporters pay in INR, USD, EUR, or AED.
  - Foreign exchange settlement via Stripe Treasury / Razorpay International.
- **Platform Fee Engine**:
  - Automated deduction of marketplace commission (e.g. 2.5% to 4%) before provider payout.

---

## 6. Provider Reputation, SLAs & Performance Badges

### The Problem in MVP
Providers are either "approved" or "pending", with no qualitative differentiation.

### Version 2.0 Capabilities
- **Verified Review & Rating System**:
  - Only exporters with confirmed, completed bookings can submit 1–5 star reviews.
  - Ratings broken down by: *Punctuality*, *Cargo Care*, *Communication*, *Billing Accuracy*.
- **Algorithmic Reliability Score (On-Time Performance %)**:
  - Automatically calculated from historical departure and arrival timestamp delta.
- **Tiered Partner Badges**:
  - 🥉 *Verified Partner* (Passed KYC)
  - 🥈 *Silver Forwarder* (10+ completed voyages, >90% OTP)
  - 🥇 *Gold Premier Carrier* (50+ completed voyages, >98% OTP, zero disputes)

---

## 7. Real-Time In-App Collaboration & Notifications

### The Problem in MVP
Exporters and providers must exchange emails or phone calls outside the platform to coordinate cargo drop-off.

### Version 2.0 Capabilities
- **Contextual Booking Chat (WebSockets)**:
  - Dedicated chat room per booking for the exporter and provider.
  - Share cargo weight slips, packaging photos, container seal numbers, and port gate passes.
- **Multi-Channel Notification Engine**:
  - WhatsApp Business API notifications (instant booking confirmation, gate-in reminders).
  - Automated transactional emails via SendGrid / AWS SES.
  - In-app notification bell with live unread badge counters.

---

## 8. 3D Container Space & Load Visualizer

### The Problem in MVP
The capacity visualizer is 1-dimensional (weight in kg only), without volume (CBM) or dimension guidance.

### Version 2.0 Capabilities
- **Weight vs. Volume (CBM) Calculation**:
  - Calculates chargeable weight according to maritime standard: `1 CBM = 1,000 kg` (or standard ocean ratio).
- **Interactive Three.js 3D Cargo Packing Visualizer**:
  - Exporters enter carton dimensions (L × W × H) and quantity.
  - 3D model shows how cargo packs inside a standard 20ft (33 CBM) or 40ft (67 CBM) container alongside existing bookings.

---

## 9. One-Click Marine Cargo Insurance

### The Problem in MVP
Cargo travels uninsured unless the exporter independently procures a commercial maritime policy.

### Version 2.0 Capabilities
- **Embedded Insurance Integration**:
  - API partnership with general maritime insurers (e.g., ICICI Lombard, Bajaj Allianz, Marsh, or Cover Genius).
  - Exporter checks "Add Cargo Protection (+₹12/kg or 0.3% invoice value)".
  - Instant policy certificate generated with booking confirmation.
  - Digital damage/claim submission portal directly from the booking detail screen.

---

## 10. Technical Architecture & Engineering Upgrades

| Architectural Area | MVP (v1.0) | Version 2.0 (v2.0) |
| :--- | :--- | :--- |
| **Backend Framework** | Synchronous FastAPI routes | FastAPI + Async SQLAlchemy 2.0 + Celery Task Queue |
| **Caching & Message Broker** | None (direct DB query) | Redis for session cache, live container availability locks, and Celery broker |
| **Database Migrations** | Initial manual sync | Alembic versioned migrations with rollback tracking |
| **Real-time Engine** | HTTP Polling | WebSockets for live chat, notification alerts, and vessel AIS radar |
| **File Storage** | Local disk uploads | AWS S3 / Cloudflare R2 with encrypted signed URLs |
| **Search Engine** | SQL `ILIKE` | PostgreSQL Full-Text Search with `pg_trgm` or Meilisearch for instant route autocomplete |
| **Concurrency Control** | Optimistic check | Database row-level locks (`SELECT FOR UPDATE`) during checkout to guarantee zero double-booking under load |
| **DevOps & Containers** | Local processes | Docker Compose (FastAPI + React + Postgres + Redis + Celery + Nginx) |

---

## Version 2.0 Release Milestones

```text
Q1: Foundation & Trust
├── Milestone 2.1: Alembic migrations, Redis caching, and concurrency locks
├── Milestone 2.2: Contextual in-app chat (WebSockets) and WhatsApp notification alerts
└── Milestone 2.3: Provider ratings, reviews, and automated On-Time Performance (OTP) scores

Q2: Digital Operations
├── Milestone 2.4: Automated e-BL generation, invoice PDF engine, and shipping document vault
├── Milestone 2.5: Multi-currency wallet and milestone-based escrow payouts
└── Milestone 2.6: Spot bidding space auction for 48-hour pre-departure clearances

Q3: Intelligence & Tracking
├── Milestone 2.7: Live AIS vessel GPS tracking with interactive Leaflet/Mapbox map
├── Milestone 2.8: 3D Three.js container space & CBM volume packing calculator
└── Milestone 2.9: One-click embedded marine cargo insurance checkout
```
