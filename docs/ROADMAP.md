# Development Roadmap

## Stage 1 - Backend Foundation

**Goal:** establish authentication and database foundation.

- [x] FastAPI
- [x] PostgreSQL
- [x] SQLAlchemy
- [x] User model
- [x] Registration
- [x] Login
- [x] Password hashing
- [x] JWT
- [x] Provider registration foundation

## Stage 2 - Roles and Provider Approval

**Goal:** complete the three-sided marketplace access model.

- [ ] Admin role
- [ ] Admin authentication
- [ ] Provider approval API
- [ ] Provider rejection API
- [ ] Provider dashboard
- [ ] Provider approval middleware/dependency

## Stage 3 - Container Marketplace

**Goal:** allow providers to supply capacity and exporters to discover it.

- [ ] Container model
- [ ] Container CRUD
- [ ] Capacity fields
- [ ] Route fields
- [ ] Departure date
- [ ] Pricing
- [ ] Availability
- [ ] Search
- [ ] Filters

## Stage 4 - Booking

**Goal:** allow exporters to reserve capacity.

- [ ] Booking model
- [ ] Booking API
- [ ] Availability recheck
- [ ] Capacity update
- [ ] Booking status
- [ ] Cancellation
- [ ] Booking history

## Stage 5 - Razorpay

**Goal:** connect booking to payment.

- [ ] Razorpay configuration
- [ ] Order creation
- [ ] Checkout integration
- [ ] Payment verification
- [ ] Payment records
- [ ] Payment status
- [ ] Failed-payment handling

## Stage 6 - React Frontend

**Goal:** provide role-specific user interfaces.

### Exporter

- [ ] Registration/login
- [ ] Search
- [ ] Listing details
- [ ] Booking
- [ ] Payment
- [ ] Booking history

### Provider

- [ ] Dashboard
- [ ] Profile
- [ ] Approval status
- [ ] Container listings
- [ ] Capacity management
- [ ] Booking management

### Admin

- [ ] Dashboard
- [ ] Provider approval
- [ ] User monitoring
- [ ] Container monitoring
- [ ] Booking monitoring
- [ ] Payment monitoring

## Stage 7 - Quality

- [ ] Unit tests
- [ ] API integration tests
- [ ] Booking concurrency tests
- [ ] Payment verification tests
- [ ] Authentication tests
- [ ] Role authorization tests

## Stage 8 - Production

- [ ] Alembic
- [ ] Environment-specific configuration
- [ ] CI/CD
- [ ] Docker
- [ ] Deployment
- [ ] Logging
- [ ] Monitoring
- [ ] Backups

---

## Next Horizon: Version 2.0 (v2.0)

For the comprehensive product and technical roadmap for **Version 2.0**, including:
- Real-time IoT / AIS vessel GPS tracking
- Multimodal logistics (Rail / ICD / Road drayage)
- Spot bidding space auction
- Automated e-BL (Bill of Lading) & shipping document vault
- B2B Escrow milestone payouts
- 3D container packing visualizer
- In-app collaboration and carrier performance ratings

👉 See the complete specification: [VERSION_2_ROADMAP.md](VERSION_2_ROADMAP.md)

