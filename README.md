# Container Space Marketplace

A three-sided logistics marketplace that connects **small exporters** with **logistics providers who have available container capacity**.

The platform allows exporters to search for suitable container space, make bookings, and pay online. Logistics providers can list and manage their available container capacity, while administrators approve providers and monitor the platform.

---

## Getting Started

### Prerequisites

Make sure the following are installed on your machine:

| Tool | Version | Notes |
|---|---|---|
| Python | 3.10+ | For the FastAPI backend |
| Node.js | 18+ | For the React frontend |
| npm | 9+ | Comes with Node.js |
| PostgreSQL | 14+ | Or use a hosted DB (e.g. Neon) |

---

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

---

### 2. Start the Backend

The backend is a **FastAPI** application using **SQLAlchemy** and **PostgreSQL**.

#### a. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

#### b. Install dependencies

```bash
pip install -r requirements.txt
```

> If there is no `requirements.txt` yet, install manually:
> ```bash
> pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv passlib[bcrypt] python-jose[cryptography]
> ```

#### c. Set up environment variables

Create a `.env` file inside the `Backend/` folder:

```env
DATABASE_URL=postgresql://<user>:<password>@<host>/<dbname>?sslmode=require
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### d. Start the server

```bash
# Run from the project root (not inside Backend/)
python -m uvicorn app.main:app --reload
```

The API will be live at: **http://localhost:8000**

Interactive API docs: **http://localhost:8000/docs**

---

### 3. Start the Frontend

The frontend is a **React** application built with **Vite**.

#### a. Install dependencies

```bash
cd frontend
npm install
```

#### b. Start the development server

```bash
npm run dev
```

The app will be live at: **http://localhost:5173**

> The frontend is pre-configured to point to `http://localhost:8000` — make sure the backend is running first.

---

### 4. Running Both Together

Open **two terminal windows** side by side:

**Terminal 1 — Backend:**
```bash
# From the project root
venv\Scripts\activate        # Windows
python -m uvicorn app.main:app --reload
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

---

### 5. Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run a specific test file
python -m pytest tests/auth_test -v
python -m pytest tests/provider_test/detail/test_provider_details_service.py -v
```

---

### 6. Seeding the Database

```bash
python -m database.seeding.seed_provider_data
```

---

### Quick Reference

| Service | URL |
|---|---|
| Frontend (React) | http://localhost:5173 |
| Backend API (FastAPI) | http://localhost:8000 |
| Swagger API Docs | http://localhost:8000/docs |
| ReDoc API Docs | http://localhost:8000/redoc |

---

## Problem Statement

Small exporters often ship relatively small quantities, such as 500 kg, that do not justify booking an entire shipping container.

Today, they may need to contact logistics providers individually to find available space. This creates several problems:

- Difficulty discovering available container capacity
- Time-consuming communication with multiple providers
- Poor visibility into pricing and availability
- Risk of capacity becoming unavailable while negotiating
- No centralized booking and payment workflow

## Proposed Solution

The platform creates a centralized marketplace for container space.

```text
                 Container Space Marketplace
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
      Exporters        Providers          Admins
          |                |                |
      Search &          List &           Approve &
      Book Space       Manage Space       Monitor
```

### Exporters

Exporters can:
- Register and authenticate
- Search available container space
- View container/capacity information
- Select suitable space
- Make a booking
- Pay through Razorpay
- Track booking status

### Providers

Logistics providers can:
- Register as providers
- Submit their business details
- Wait for admin approval
- List available container capacity
- Manage their listings
- Manage bookings related to their containers

### Admins

Administrators can:
- Authenticate
- Review provider registrations
- Approve or reject providers
- Monitor platform activity
- Oversee containers and bookings
- Monitor payment/booking status

---

# MVP Scope

The MVP contains **15 must-have features**.

## Authentication & Access

1. User registration
2. User login
3. JWT-based authentication
4. Role-based access control

## Provider Management

5. Provider registration
6. Admin provider approval/rejection

## Container Marketplace

7. Provider container/capacity listing
8. Container availability management
9. Exporter container-space search
10. Search/filtering

## Booking & Payment

11. Booking creation
12. Real-time availability validation
13. Booking management/status tracking
14. Razorpay payment integration
15. Basic admin monitoring

The MVP should prioritize these features before adding non-essential functionality.

---

# Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Backend | Python + FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| API style | REST |
| Payment gateway | Razorpay |
| API documentation | OpenAPI / Swagger |
| Server | Uvicorn |

---

# System Architecture

```text
┌──────────────────────────────────────────┐
│              React Frontend              │
│                                          │
│ Exporter UI | Provider UI | Admin UI     │
└────────────────────┬─────────────────────┘
                     │
                  REST API
                     │
                  JWT Auth
                     │
                     ▼
┌──────────────────────────────────────────┐
│            FastAPI Backend               │
│                                          │
│  Authentication                          │
│  Providers                               │
│  Containers                              │
│  Bookings                                │
│  Payments                                │
│  Admin                                   │
│  Business Rules                          │
└────────────────────┬─────────────────────┘
                     │
                  SQLAlchemy
                     │
                     ▼
┌──────────────────────────────────────────┐
│               PostgreSQL                 │
│                                          │
│ Users | Providers | Containers           │
│ Bookings | Payments | ...                │
└──────────────────────────────────────────┘

                     │
                     │ Payment API
                     ▼
              ┌──────────────┐
              │   Razorpay   │
              └──────────────┘
```

The architecture follows a clean three-tier model:

```text
Presentation Layer
       ↓
Application / API Layer
       ↓
Data Layer
```

See [Architecture](docs/ARCHITECTURE.md).

---

# User Roles

## Exporter

Primary objective: **find and book container space.**

Permissions:

- Register/login
- Search containers
- View availability
- Create booking
- Make payment
- View own bookings
- Track booking status

## Provider

Primary objective: **offer available container capacity.**

Permissions:

- Register/login
- Submit provider details
- View approval status
- Create container listings after approval
- Update availability
- Manage own listings
- View/manage relevant bookings

## Admin

Primary objective: **operate and control the marketplace.**

Permissions:

- Login
- View users
- Review providers
- Approve/reject providers
- Monitor containers
- Monitor bookings
- Monitor payments
- Manage platform-level issues

---

# Core User Flows

## Exporter Flow

```text
Register
   ↓
Login
   ↓
Search container space
   ↓
Apply filters
   ↓
View available capacity
   ↓
Select container
   ↓
Enter booking details
   ↓
Check availability
   ↓
Create booking
   ↓
Razorpay payment
   ↓
Payment confirmation
   ↓
Booking confirmed
```

## Provider Flow

```text
Register
   ↓
Submit provider information
   ↓
approval_status = pending
   ↓
Admin review
   ↓
Approved?
  /   No     Yes
|       |
Reject  Provider dashboard
        ↓
   Add container capacity
        ↓
   Manage availability
        ↓
   Receive bookings
        ↓
   Manage booking status
```

## Admin Flow

```text
Admin Login
    ↓
Admin Dashboard
    ↓
Review providers
    ↓
Approve / Reject
    ↓
Monitor platform
    ├── Providers
    ├── Containers
    ├── Bookings
    └── Payments
```

---

# Project Structure

The intended full-stack structure is:

```text
project/
│
├── README.md
│
├── docs/
│   ├── REQUIREMENTS.md
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── DATABASE.md
│   ├── BUSINESS_RULES.md
│   ├── USER_FLOWS.md
│   ├── SETUP.md
│   ├── SECURITY.md
│   └── ROADMAP.md
│
├── frontend/
│   └── React application
│
└── backend/
    └── FastAPI application
```

The current backend repository is being developed toward this architecture.

---

# Current Backend Status

The existing backend already provides the foundation for:

- FastAPI application
- PostgreSQL connection
- SQLAlchemy models
- User registration
- Login
- Password hashing
- JWT authentication
- Protected routes
- Provider registration
- Provider role authorization
- Provider approval-status field

The marketplace functionality is the next major development stage:

- Container management
- Search
- Booking
- Availability validation
- Payments
- Admin controls

See [Roadmap](docs/ROADMAP.md).

---

# API Domains

The planned REST API is organized around these domains:

```text
/auth
/providers
/containers
/bookings
/payments
/admin
```

Detailed API contracts are documented in [API Documentation](docs/API.md).

---

# Security

The platform uses JWT authentication and role-based authorization.

Important security requirements:

- Never store plaintext passwords
- Never commit `.env` files
- Keep JWT secrets outside source code
- Validate user roles on protected operations
- Validate container availability before booking
- Verify payment responses using Razorpay's server-side mechanisms
- Use HTTPS in production
- Use database transactions for booking/availability updates

See [Security](docs/SECURITY.md).

---

# Development Roadmap

## Phase 1: Foundation

- [x] FastAPI setup
- [x] PostgreSQL integration
- [x] SQLAlchemy
- [x] User registration
- [x] Login
- [x] Password hashing
- [x] JWT authentication
- [x] Provider registration

## Phase 2: Provider Management

- [ ] Admin role
- [ ] Provider approval/rejection
- [ ] Provider dashboard
- [ ] Provider profile management

## Phase 3: Container Marketplace

- [ ] Container model
- [ ] Container capacity model
- [ ] Container listing
- [ ] Availability management
- [ ] Search
- [ ] Filters

## Phase 4: Booking

- [ ] Booking model
- [ ] Booking creation
- [ ] Availability locking/validation
- [ ] Booking status
- [ ] Cancellation
- [ ] Booking history

## Phase 5: Payments

- [ ] Razorpay order creation
- [ ] Payment checkout
- [ ] Server-side payment verification
- [ ] Payment status
- [ ] Booking/payment reconciliation

## Phase 6: Administration

- [ ] Admin dashboard
- [ ] Provider approval
- [ ] Platform monitoring
- [ ] Booking monitoring
- [ ] Payment monitoring

## Phase 7: Production

- [ ] Automated tests
- [ ] Database migrations
- [ ] CI/CD
- [ ] Secure secret management
- [ ] Production deployment
- [ ] Logging
- [ ] Monitoring

---

# Future Scope

Possible features after the MVP:

- Route-based search
- International shipping integrations
- Notifications
- Email/SMS alerts
- Ratings and reviews
- Advanced provider analytics
- Automated pricing
- Recommendation engine
- Multiple payment methods
- Document management
- Shipment tracking
- Mobile application
- Multi-language support

---

# Documentation

| Document | Purpose |
|---|---|
| [Requirements](docs/REQUIREMENTS.md) | Functional and non-functional requirements |
| [Architecture](docs/ARCHITECTURE.md) | System architecture and components |
| [API](docs/API.md) | REST API contract |
| [Database](docs/DATABASE.md) | Database entities and relationships |
| [Business Rules](docs/BUSINESS_RULES.md) | Marketplace rules |
| [User Flows](docs/USER_FLOWS.md) | Exporter/provider/admin workflows |
| [Setup](docs/SETUP.md) | Local development setup |
| [Security](docs/SECURITY.md) | Authentication and security |
| [Roadmap](docs/ROADMAP.md) | Development plan |

---

# License

Add the project's selected license before public release.
