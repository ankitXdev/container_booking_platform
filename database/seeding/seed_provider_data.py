import sys
from pathlib import Path

BACKEND_PATH = Path(__file__).resolve().parents[2] / "Backend"
sys.path.insert(0, str(BACKEND_PATH))

from Backend.app.config.database import SessionLocal
from Backend.app.models.user_model import users
from Backend.app.models.provider_details_model import provider_details
from Backend.app.utils.password import hash_password


def seed_provider_data():
    db = SessionLocal()

    try:
        providers_data = [
            {
                "name": "Rajesh Sharma",
                "email": "rajesh.sharma@example.com",
                "business_name": "Sharma Agro Services",
                "business_address": "Lucknow, Uttar Pradesh",
                "contact": "9876543210",
                "approval_status": "approved",
            },
            {
                "name": "Amit Sharma",
                "email": "amit.sharma@example.com",
                "business_name": "Sharma Agro Services",
                "business_address": "Kanpur, Uttar Pradesh",
                "contact": "9123456780",
                "approval_status": "approved",
            },
            {
                "name": "Vikash Kumar",
                "email": "vikash.kumar@example.com",
                "business_name": "Sharma Seeds and Fertilizers",
                "business_address": "Prayagraj, Uttar Pradesh",
                "contact": "9988776655",
                "approval_status": "approved",
            },
            {
                "name": "Suresh Verma",
                "email": "suresh.verma@example.com",
                "business_name": "Verma Agricultural Equipment",
                "business_address": "Varanasi, Uttar Pradesh",
                "contact": "9012345678",
                "approval_status": "approved",
            },
            {
                "name": "Rohit Singh",
                "email": "rohit.singh@example.com",
                "business_name": "Singh Agro Traders",
                "business_address": "Agra, Uttar Pradesh",
                "contact": "9876543211",
                "approval_status": "approved",
            },
            {
                "name": "Manoj Gupta",
                "email": "manoj.gupta@example.com",
                "business_name": "Gupta Farm Supplies",
                "business_address": "Meerut, Uttar Pradesh",
                "contact": "9876543212",
                "approval_status": "pending",
            },
        ]

        for data in providers_data:

            # Check whether the user already exists
            existing_user = (
                db.query(users)
                .filter(users.email == data["email"])
                .first()
            )

            if existing_user:
                user = existing_user
                print(f"User already exists: {data['email']}")

            else:
                user = users(
                    name=data["name"],
                    email=data["email"],
                    password_hash=hash_password("Test@123"),
                    role="provider",
                    status="active",
                )

                db.add(user)
                db.flush()

                print(f"Created user: {data['email']}")

            # Check whether provider profile already exists
            existing_provider = (
                db.query(provider_details)
                .filter(
                    provider_details.user_id == user.user_id
                )
                .first()
            )

            if existing_provider:
                print(
                    f"Provider already exists: "
                    f"{data['business_name']} "
                    f"({data['email']})"
                )
                continue

            provider = provider_details(
                user_id=user.user_id,
                business_name=data["business_name"],
                business_address=data["business_address"],
                contact=data["contact"],
                approval_status=data["approval_status"],
            )

            db.add(provider)

            print(
                f"Created provider: "
                f"{data['business_name']} "
                f"({data['approval_status']})"
            )

        db.commit()

        print("\nProvider seed data inserted successfully.")

    except Exception as e:
        db.rollback()
        print(f"\nError while seeding provider data: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_provider_data()