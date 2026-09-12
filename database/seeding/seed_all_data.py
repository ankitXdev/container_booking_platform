import sys
from pathlib import Path
from datetime import datetime, timedelta

ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT_DIR / "Backend"

for p in (str(ROOT_DIR), str(BACKEND_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from app.config.database import SessionLocal
    from app.models.user_model import users
    from app.models.provider_details_model import provider_details
    from app.models.container_model import container
    from app.models.booking_model import booking
    from app.models.payment_model import payment
    from app.models.exporter_document_model import exporter_document
    from app.models.provider_document_model import provider_document
    from app.utils.password import hash_password
except ImportError:
    from Backend.app.config.database import SessionLocal
    from Backend.app.models.user_model import users
    from Backend.app.models.provider_details_model import provider_details
    from Backend.app.models.container_model import container
    from Backend.app.models.booking_model import booking
    from Backend.app.models.payment_model import payment
    from Backend.app.models.exporter_document_model import exporter_document
    from Backend.app.models.provider_document_model import provider_document
    from Backend.app.utils.password import hash_password


def seed_all():
    db = SessionLocal()
    print(">>> Starting database seeding for Cargo Space Booking Platform...\n")

    try:
        # =========================================================================
        # 1. SEED USERS (Admin, Exporters, Providers)
        # =========================================================================
        user_definitions = [
            # Platform Admin
            {
                "name": "Platform Administrator",
                "email": "admin@cargobooking.com",
                "password": "Admin@123password",
                "role": "admin",
            },
            # Exporters
            {
                "name": "Ankit Exporters Pvt Ltd",
                "email": "ankit@example.com",
                "password": "ankit1234567891011121",
                "role": "exporter",
            },
            {
                "name": "Gujarat Textiles & Silk Export",
                "email": "priya.patel@gujarattextiles.com",
                "password": "Exporter@123",
                "role": "exporter",
            },
            {
                "name": "Malabar Heritage Spices",
                "email": "arun.nair@malabarspices.in",
                "password": "Exporter@123",
                "role": "exporter",
            },
            # Logistics Providers
            {
                "name": "OceanLine Freight Solutions",
                "email": "contact@oceanlinefreight.com",
                "password": "Provider@123",
                "role": "provider",
            },
            {
                "name": "Global Swift Cargo Movers",
                "email": "operations@globalswift.com",
                "password": "Provider@123",
                "role": "provider",
            },
            {
                "name": "Blue Anchor Marine Logistics",
                "email": "marine@blueanchor.in",
                "password": "Provider@123",
                "role": "provider",
            },
            {
                "name": "Kandla Gateway Shipping",
                "email": "info@kandlashipping.com",
                "password": "Provider@123",
                "role": "provider",
            },
            {
                "name": "Coastway Express Cargo",
                "email": "admin@coastwaycargo.com",
                "password": "Provider@123",
                "role": "provider",
            },
        ]

        created_users = {}
        for u_data in user_definitions:
            user = db.query(users).filter(users.email == u_data["email"]).first()
            if not user:
                user = users(
                    name=u_data["name"],
                    email=u_data["email"],
                    password_hash=hash_password(u_data["password"]),
                    role=u_data["role"],
                    status="active",
                )
                db.add(user)
                db.flush()
                print(f"  [+] Created User: {u_data['email']} ({u_data['role']})")
            else:
                print(f"  [~] User already exists: {u_data['email']}")
            created_users[u_data["email"]] = user

        # =========================================================================
        # 2. SEED PROVIDER PROFILES
        # =========================================================================
        provider_definitions = [
            {
                "user_email": "contact@oceanlinefreight.com",
                "business_name": "OceanLine Freight Solutions Ltd.",
                "business_address": "Terminal 4, JNPT Port Area, Navi Mumbai, Maharashtra",
                "contact": "+91-9820012345",
                "approval_status": "approved",
            },
            {
                "user_email": "operations@globalswift.com",
                "business_name": "Global Swift Cargo Movers",
                "business_address": "Harbour Gate 2, Chennai Port, Tamil Nadu",
                "contact": "+91-9440056789",
                "approval_status": "approved",
            },
            {
                "user_email": "marine@blueanchor.in",
                "business_name": "Blue Anchor Marine Logistics",
                "business_address": "Strand Road, Kidderpore Dock, Kolkata, West Bengal",
                "contact": "+91-9830098765",
                "approval_status": "approved",
            },
            {
                "user_email": "info@kandlashipping.com",
                "business_name": "Kandla Gateway Shipping Co.",
                "business_address": "Cargo Jetty Zone, Deendayal Port, Kandla, Gujarat",
                "contact": "+91-9825065432",
                "approval_status": "pending",  # Pending admin review
            },
            {
                "user_email": "admin@coastwaycargo.com",
                "business_name": "Coastway Express Cargo",
                "business_address": "Willingdon Island, Cochin Port, Kerala",
                "contact": "+91-9847033221",
                "approval_status": "rejected",  # Rejected provider
            },
        ]

        created_providers = {}
        for p_data in provider_definitions:
            usr = created_users[p_data["user_email"]]
            prov = (
                db.query(provider_details)
                .filter(provider_details.user_id == usr.user_id)
                .first()
            )
            if not prov:
                prov = provider_details(
                    user_id=usr.user_id,
                    business_name=p_data["business_name"],
                    business_address=p_data["business_address"],
                    contact=p_data["contact"],
                    approval_status=p_data["approval_status"],
                )
                db.add(prov)
                db.flush()
                print(
                    f"  [+] Created Provider Profile: {p_data['business_name']} ({p_data['approval_status']})"
                )
            else:
                print(f"  [~] Provider already exists: {p_data['business_name']}")
            created_providers[p_data["user_email"]] = prov

        # =========================================================================
        # 3. SEED CONTAINER LISTINGS
        # =========================================================================
        now = datetime.utcnow()
        container_definitions = [
            {
                "provider_email": "contact@oceanlinefreight.com",
                "origin": "Mumbai (JNPT)",
                "destination": "Dubai (Jebel Ali)",
                "departure_date": now + timedelta(days=5),
                "total_capacity_kg": 25000.0,
                "available_capacity_kg": 18500.0,
                "price_per_kg": 18.50,
                "is_available": True,
            },
            {
                "provider_email": "contact@oceanlinefreight.com",
                "origin": "Mumbai (JNPT)",
                "destination": "Rotterdam (Netherlands)",
                "departure_date": now + timedelta(days=12),
                "total_capacity_kg": 30000.0,
                "available_capacity_kg": 24000.0,
                "price_per_kg": 36.00,
                "is_available": True,
            },
            {
                "provider_email": "operations@globalswift.com",
                "origin": "Chennai Port",
                "destination": "Singapore (PSA)",
                "departure_date": now + timedelta(days=7),
                "total_capacity_kg": 20000.0,
                "available_capacity_kg": 12000.0,
                "price_per_kg": 22.00,
                "is_available": True,
            },
            {
                "provider_email": "operations@globalswift.com",
                "origin": "Chennai Port",
                "destination": "Port Klang (Malaysia)",
                "departure_date": now + timedelta(days=15),
                "total_capacity_kg": 16000.0,
                "available_capacity_kg": 0.0,
                "price_per_kg": 20.00,
                "is_available": False,  # Fully booked
            },
            {
                "provider_email": "marine@blueanchor.in",
                "origin": "Kolkata Port",
                "destination": "Colombo (Sri Lanka)",
                "departure_date": now + timedelta(days=9),
                "total_capacity_kg": 18000.0,
                "available_capacity_kg": 16000.0,
                "price_per_kg": 14.00,
                "is_available": True,
            },
            {
                "provider_email": "marine@blueanchor.in",
                "origin": "Kolkata Port",
                "destination": "Chittagong (Bangladesh)",
                "departure_date": now + timedelta(days=4),
                "total_capacity_kg": 15000.0,
                "available_capacity_kg": 11000.0,
                "price_per_kg": 11.50,
                "is_available": True,
            },
        ]

        created_containers = []
        for c_data in container_definitions:
            prov = created_providers[c_data["provider_email"]]
            existing_c = (
                db.query(container)
                .filter(
                    container.provider_id == prov.provider_id,
                    container.origin == c_data["origin"],
                    container.destination == c_data["destination"],
                )
                .first()
            )
            if not existing_c:
                new_c = container(
                    provider_id=prov.provider_id,
                    origin=c_data["origin"],
                    destination=c_data["destination"],
                    departure_date=c_data["departure_date"],
                    total_capacity_kg=c_data["total_capacity_kg"],
                    available_capacity_kg=c_data["available_capacity_kg"],
                    price_per_kg=c_data["price_per_kg"],
                    is_available=c_data["is_available"],
                )
                db.add(new_c)
                db.flush()
                print(
                    f"  [+] Created Container #{new_c.container_id}: {new_c.origin} -> {new_c.destination} ({new_c.available_capacity_kg} kg available)"
                )
                created_containers.append(new_c)
            else:
                print(
                    f"  [~] Container already exists: {existing_c.origin} -> {existing_c.destination}"
                )
                created_containers.append(existing_c)

        # =========================================================================
        # 4. SEED SAMPLE BOOKINGS & PAYMENTS
        # =========================================================================
        exporter_ankit = created_users["ankit@example.com"]
        exporter_priya = created_users["priya.patel@gujarattextiles.com"]
        exporter_arun = created_users["arun.nair@malabarspices.in"]

        booking_definitions = [
            # 1. Confirmed booking with completed payment (Ankit on Mumbai -> Dubai)
            {
                "container": created_containers[0],
                "exporter": exporter_ankit,
                "booked_capacity_kg": 6500.0,
                "status": "confirmed",
                "payment": {
                    "razorpay_order_id": "order_mock_001_mumbai",
                    "razorpay_payment_id": "pay_mock_001_success",
                    "razorpay_signature": "sig_mock_verified_001",
                    "status": "paid",
                },
            },
            # 2. Confirmed booking with completed payment (Priya on Chennai -> Singapore)
            {
                "container": created_containers[2],
                "exporter": exporter_priya,
                "booked_capacity_kg": 8000.0,
                "status": "confirmed",
                "payment": {
                    "razorpay_order_id": "order_mock_002_chennai",
                    "razorpay_payment_id": "pay_mock_002_success",
                    "razorpay_signature": "sig_mock_verified_002",
                    "status": "paid",
                },
            },
            # 3. Pending payment booking (Ankit on Kolkata -> Colombo) - Ready to test payment in UI!
            {
                "container": created_containers[4],
                "exporter": exporter_ankit,
                "booked_capacity_kg": 2000.0,
                "status": "pending",
                "payment": None,
            },
            # 4. Cancelled booking
            {
                "container": created_containers[1],
                "exporter": exporter_arun,
                "booked_capacity_kg": 1500.0,
                "status": "cancelled",
                "payment": None,
            },
        ]

        for b_data in booking_definitions:
            c_target = b_data["container"]
            e_user = b_data["exporter"]
            total_price = round(b_data["booked_capacity_kg"] * c_target.price_per_kg, 2)

            existing_b = (
                db.query(booking)
                .filter(
                    booking.container_id == c_target.container_id,
                    booking.exporter_id == e_user.user_id,
                    booking.status == b_data["status"],
                )
                .first()
            )

            if not existing_b:
                new_b = booking(
                    container_id=c_target.container_id,
                    exporter_id=e_user.user_id,
                    booked_capacity_kg=b_data["booked_capacity_kg"],
                    total_price=total_price,
                    status=b_data["status"],
                )
                db.add(new_b)
                db.flush()
                print(
                    f"  [+] Created Booking #{new_b.booking_id}: {b_data['booked_capacity_kg']} kg on Container #{c_target.container_id} ({new_b.status})"
                )

                if b_data["payment"]:
                    pay_info = b_data["payment"]
                    new_pay = payment(
                        booking_id=new_b.booking_id,
                        razorpay_order_id=pay_info["razorpay_order_id"],
                        razorpay_payment_id=pay_info["razorpay_payment_id"],
                        razorpay_signature=pay_info["razorpay_signature"],
                        amount=total_price,
                        currency="INR",
                        status=pay_info["status"],
                    )
                    db.add(new_pay)
                    db.flush()
                    print(
                        f"      |-- Created Payment #{new_pay.payment_id}: INR {total_price} ({pay_info['status']})"
                    )
            else:
                print(f"  [~] Booking already exists for Exporter #{e_user.user_id} on Container #{c_target.container_id}")

        # =========================================================================
        # 5. SEED COMPLIANCE DOCUMENTS (Exporters and Providers)
        # =========================================================================
        print("\n>>> Seeding Compliance Documents for Exporters & Providers...")
        admin_user = created_users.get("admin@cargobooking.com")
        admin_id = admin_user.user_id if admin_user else None

        # Exporter docs
        exporter_docs_def = [
            {
                "user": exporter_ankit,
                "type": "IEC",
                "number": "0388012345",
                "url": "/uploads/documents/sample_ankit_iec.pdf",
                "status": "VERIFIED",
                "verified_by": admin_id,
            },
            {
                "user": exporter_priya,
                "type": "GST",
                "number": "24AAACG1234F1ZP",
                "url": "/uploads/documents/sample_priya_gst.pdf",
                "status": "VERIFIED",
                "verified_by": admin_id,
            },
            {
                "user": exporter_arun,
                "type": "PAN",
                "number": "ABCDE1234F",
                "url": "/uploads/documents/sample_arun_pan.pdf",
                "status": "PENDING",
                "verified_by": None,
            },
        ]

        for ed in exporter_docs_def:
            if not ed["user"]:
                continue
            existing_ed = (
                db.query(exporter_document)
                .filter(
                    exporter_document.user_id == ed["user"].user_id,
                    exporter_document.document_type == ed["type"]
                )
                .first()
            )
            if not existing_ed:
                new_ed = exporter_document(
                    user_id=ed["user"].user_id,
                    document_type=ed["type"],
                    document_number=ed["number"],
                    document_url=ed["url"],
                    status=ed["status"],
                    verified_by=ed["verified_by"],
                    verified_at=now if ed["status"] == "VERIFIED" else None
                )
                db.add(new_ed)
                db.flush()
                print(f"  [+] Created Exporter Document #{new_ed.document_id} ({ed['type']}) for User #{ed['user'].user_id} [{ed['status']}]")

        # Provider docs
        prov_ocean = created_providers.get("contact@oceanlinefreight.com")
        prov_swift = created_providers.get("operations@globalswift.com")
        prov_blue = created_providers.get("marine@blueanchor.in")

        provider_docs_def = [
            {
                "provider": prov_ocean,
                "type": "MTO_LICENSE",
                "number": "MTO/2023/10892",
                "url": "/uploads/documents/sample_oceanline_mto.pdf",
                "status": "VERIFIED",
                "verified_by": admin_id,
            },
            {
                "provider": prov_swift,
                "type": "GST",
                "number": "33AAACG9876Q1Z9",
                "url": "/uploads/documents/sample_globalswift_gst.pdf",
                "status": "VERIFIED",
                "verified_by": admin_id,
            },
            {
                "provider": prov_blue,
                "type": "FREIGHT_INSURANCE",
                "number": "INS/MAR/99823",
                "url": "/uploads/documents/sample_blueanchor_ins.pdf",
                "status": "PENDING",
                "verified_by": None,
            },
        ]

        for pd in provider_docs_def:
            if not pd["provider"]:
                continue
            existing_pd = (
                db.query(provider_document)
                .filter(
                    provider_document.provider_id == pd["provider"].provider_id,
                    provider_document.document_type == pd["type"]
                )
                .first()
            )
            if not existing_pd:
                new_pd = provider_document(
                    provider_id=pd["provider"].provider_id,
                    document_type=pd["type"],
                    document_number=pd["number"],
                    document_url=pd["url"],
                    status=pd["status"],
                    verified_by=pd["verified_by"],
                    verified_at=now if pd["status"] == "VERIFIED" else None
                )
                db.add(new_pd)
                db.flush()
                print(f"  [+] Created Provider Document #{new_pd.document_id} ({pd['type']}) for Provider #{pd['provider'].provider_id} [{pd['status']}]")

        db.commit()

        # =========================================================================
        # 6. SEED HISTORICAL VOYAGES & COMPLETED BOOKINGS (for provider stats)
        # =========================================================================
        print("\n>>> Seeding Historical Voyages & Completed Bookings for Provider Stats...")

        # Re-fetch providers in case they were already in DB on first run
        prov_ocean_fresh = db.query(provider_details).filter(
            provider_details.user_id == created_users["contact@oceanlinefreight.com"].user_id
        ).first()
        prov_swift_fresh = db.query(provider_details).filter(
            provider_details.user_id == created_users["operations@globalswift.com"].user_id
        ).first()
        prov_blue_fresh = db.query(provider_details).filter(
            provider_details.user_id == created_users["marine@blueanchor.in"].user_id
        ).first()

        historical_voyages = [
            # ── OceanLine Freight: 4 past voyages ──────────────────────────────
            {
                "provider": prov_ocean_fresh,
                "origin": "Mumbai (JNPT)", "destination": "Abu Dhabi (Khalifa)",
                "departure_date": now - timedelta(days=90),
                "total_capacity_kg": 25000.0, "available_capacity_kg": 0.0,
                "price_per_kg": 16.0, "is_available": False,
                "bookings": [
                    {"exporter": exporter_ankit, "kg": 12000.0},
                    {"exporter": exporter_priya, "kg": 9500.0},
                    {"exporter": exporter_arun,  "kg": 3500.0},
                ],
            },
            {
                "provider": prov_ocean_fresh,
                "origin": "Mumbai (JNPT)", "destination": "Hamburg (Germany)",
                "departure_date": now - timedelta(days=55),
                "total_capacity_kg": 30000.0, "available_capacity_kg": 0.0,
                "price_per_kg": 38.0, "is_available": False,
                "bookings": [
                    {"exporter": exporter_priya, "kg": 14000.0},
                    {"exporter": exporter_ankit, "kg": 16000.0},
                ],
            },
            {
                "provider": prov_ocean_fresh,
                "origin": "Nhava Sheva (JNPT)", "destination": "Colombo (Sri Lanka)",
                "departure_date": now - timedelta(days=30),
                "total_capacity_kg": 18000.0, "available_capacity_kg": 2000.0,
                "price_per_kg": 14.5, "is_available": False,
                "bookings": [
                    {"exporter": exporter_arun, "kg": 8000.0},
                    {"exporter": exporter_ankit, "kg": 8000.0},
                ],
            },

            # ── Global Swift Cargo: 3 past voyages ────────────────────────────
            {
                "provider": prov_swift_fresh,
                "origin": "Chennai Port", "destination": "Colombo (Sri Lanka)",
                "departure_date": now - timedelta(days=80),
                "total_capacity_kg": 20000.0, "available_capacity_kg": 0.0,
                "price_per_kg": 13.0, "is_available": False,
                "bookings": [
                    {"exporter": exporter_priya, "kg": 11000.0},
                    {"exporter": exporter_arun,  "kg": 9000.0},
                ],
            },
            {
                "provider": prov_swift_fresh,
                "origin": "Chennai Port", "destination": "Kuala Lumpur (Port Klang)",
                "departure_date": now - timedelta(days=45),
                "total_capacity_kg": 16000.0, "available_capacity_kg": 0.0,
                "price_per_kg": 19.0, "is_available": False,
                "bookings": [
                    {"exporter": exporter_ankit, "kg": 7500.0},
                    {"exporter": exporter_priya, "kg": 8500.0},
                ],
            },
            {
                "provider": prov_swift_fresh,
                "origin": "Tuticorin Port", "destination": "Singapore (PSA)",
                "departure_date": now - timedelta(days=20),
                "total_capacity_kg": 14000.0, "available_capacity_kg": 1500.0,
                "price_per_kg": 21.0, "is_available": False,
                "bookings": [
                    {"exporter": exporter_arun, "kg": 6000.0},
                    {"exporter": exporter_priya, "kg": 6500.0},
                ],
            },

            # ── Blue Anchor Marine: 3 past voyages ────────────────────────────
            {
                "provider": prov_blue_fresh,
                "origin": "Kolkata Port", "destination": "Mongla (Bangladesh)",
                "departure_date": now - timedelta(days=70),
                "total_capacity_kg": 12000.0, "available_capacity_kg": 0.0,
                "price_per_kg": 10.0, "is_available": False,
                "bookings": [
                    {"exporter": exporter_ankit, "kg": 6000.0},
                    {"exporter": exporter_arun,  "kg": 6000.0},
                ],
            },
            {
                "provider": prov_blue_fresh,
                "origin": "Kolkata Port", "destination": "Yangon (Myanmar)",
                "departure_date": now - timedelta(days=40),
                "total_capacity_kg": 15000.0, "available_capacity_kg": 0.0,
                "price_per_kg": 12.0, "is_available": False,
                "bookings": [
                    {"exporter": exporter_priya, "kg": 9000.0},
                    {"exporter": exporter_ankit, "kg": 6000.0},
                ],
            },
            {
                "provider": prov_blue_fresh,
                "origin": "Haldia Port", "destination": "Ho Chi Minh City (Vietnam)",
                "departure_date": now - timedelta(days=15),
                "total_capacity_kg": 10000.0, "available_capacity_kg": 500.0,
                "price_per_kg": 17.5, "is_available": False,
                "bookings": [
                    {"exporter": exporter_arun, "kg": 5000.0},
                    {"exporter": exporter_priya, "kg": 4500.0},
                ],
            },
        ]

        booking_counter = 900  # Start IDs far from existing to avoid clashes
        for voyage in historical_voyages:
            prov = voyage["provider"]
            if not prov:
                continue

            # Check if this historical voyage already exists
            existing_hist = (
                db.query(container)
                .filter(
                    container.provider_id == prov.provider_id,
                    container.origin == voyage["origin"],
                    container.destination == voyage["destination"],
                )
                .first()
            )
            if existing_hist:
                hist_container = existing_hist
                print(f"  [~] Historical voyage already exists: {voyage['origin']} -> {voyage['destination']}")
            else:
                hist_container = container(
                    provider_id=prov.provider_id,
                    origin=voyage["origin"],
                    destination=voyage["destination"],
                    departure_date=voyage["departure_date"],
                    total_capacity_kg=voyage["total_capacity_kg"],
                    available_capacity_kg=voyage["available_capacity_kg"],
                    price_per_kg=voyage["price_per_kg"],
                    is_available=voyage["is_available"],
                )
                db.add(hist_container)
                db.flush()
                print(f"  [+] Created Historical Voyage #{hist_container.container_id}: {voyage['origin']} -> {voyage['destination']}")

            # Seed the bookings for this voyage
            for bk in voyage["bookings"]:
                total_price = round(bk["kg"] * voyage["price_per_kg"], 2)
                existing_bk = (
                    db.query(booking)
                    .filter(
                        booking.container_id == hist_container.container_id,
                        booking.exporter_id == bk["exporter"].user_id,
                        booking.status == "confirmed",
                    )
                    .first()
                )
                if existing_bk:
                    print(f"      [~] Booking already exists for exporter #{bk['exporter'].user_id} on voyage #{hist_container.container_id}")
                else:
                    hist_booking = booking(
                        container_id=hist_container.container_id,
                        exporter_id=bk["exporter"].user_id,
                        booked_capacity_kg=bk["kg"],
                        total_price=total_price,
                        status="confirmed",
                    )
                    db.add(hist_booking)
                    db.flush()
                    print(f"      [+] Created Historical Booking #{hist_booking.booking_id}: {bk['kg']} kg ({total_price} INR) — Exporter #{bk['exporter'].user_id}")

        db.commit()
        print("\n[OK] Database seeding finished successfully!")


    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Error during database seeding: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
