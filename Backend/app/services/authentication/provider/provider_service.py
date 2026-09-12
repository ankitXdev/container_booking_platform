from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.models.provider_details_model import provider_details
from app.models.container_model import container
from app.models.booking_model import booking
from app.models.provider_document_model import provider_document


def register_provider(provider, current_user, db: Session):
    
    # 1. User must have provider role
    if current_user.role != "provider":
        raise HTTPException(
            status_code=403,
            detail="Only users with provider role can register as a provider"
        )

    # 2. Check if this user already has a provider profile
    existing_provider = (
        db.query(provider_details)
        .filter(
            provider_details.user_id == current_user.user_id
        )
        .first()
    )

    if existing_provider:
        raise HTTPException(
            status_code=409,
            detail="Provider profile already exists"
        )

    # 3. Create provider profile
    new_provider = provider_details(
        user_id=current_user.user_id,
        business_name=provider.business_name,
        contact=provider.contact,
        business_address=provider.business_address,
        approval_status="pending"
    )

    # 4. Save to database
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)

    # 5. Return registration response
    return {
        "message": "Provider registration successful",
        "provider_id": new_provider.provider_id,
        "approval_status": new_provider.approval_status
    }

def search_provider(business_name: str, db: Session):
    business_name = business_name.strip()

    providers = (
        db.query(provider_details)
        .filter(
            provider_details.business_name.ilike(f"%{business_name}%"),
            provider_details.approval_status == "approved"
        )
        .all()
    )

    result = []

    for provider in providers:
        result.append({
            "provider_id": provider.provider_id,
            "business_name": provider.business_name,
            "business_address": provider.business_address,
            "contact": provider.contact,
            "email": provider.user.email
        })

    return result

def update_provider(
    provider_id: int,
    provider,
    current_user,
    db: Session
):
    # 1. Find the provider
    existing_provider = (
        db.query(provider_details)
        .filter(
            provider_details.provider_id == provider_id
        )
        .first()
    )

    if not existing_provider:
        raise HTTPException(
            status_code=404,
            detail="Provider not found"
        )

    # 2. Only the owner can update the provider profile
    if existing_provider.user_id != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to update this provider profile"
        )

    # 3. Update allowed fields
    existing_provider.business_name = provider.business_name
    existing_provider.business_address = provider.business_address
    existing_provider.contact = provider.contact

    # 4. Do NOT modify approval_status

    # 5. Save changes
    db.commit()
    db.refresh(existing_provider)

    return {
        "message": "Provider profile updated successfully"
    }

def get_provider_details(
    provider_id: int,
    current_user,
    db: Session
):
    # 1. Find the provider
    existing_provider = (
        db.query(provider_details)
        .filter(
            provider_details.provider_id == provider_id
        )
        .first()
    )

    # 2. Provider does not exist
    if not existing_provider:
        raise HTTPException(
            status_code=404,
            detail="Provider not found"
        )

    # 3. Normal users can only view approved providers
    if existing_provider.approval_status != "approved":
        raise HTTPException(
            status_code=404,
            detail="Provider not found"
        )

    # 4. Aggregate container stats
    all_containers = (
        db.query(container)
        .filter(container.provider_id == provider_id)
        .all()
    )

    total_containers_count = len(all_containers)
    active_containers_count = sum(1 for c in all_containers if c.is_available)

    # Unique routes (origin, destination) across all containers
    seen_routes = set()
    serviced_routes = []
    for c in all_containers:
        key = (c.origin, c.destination)
        if key not in seen_routes:
            seen_routes.add(key)
            serviced_routes.append({"origin": c.origin, "destination": c.destination})

    # Container IDs for booking lookups
    container_ids = [c.container_id for c in all_containers]

    # 5. Aggregate booking stats on this provider's containers
    completed_bookings_count = 0
    total_cargo_handled_kg = 0.0

    if container_ids:
        completed_bookings = (
            db.query(booking)
            .filter(
                booking.container_id.in_(container_ids),
                booking.status == "confirmed"
            )
            .all()
        )
        completed_bookings_count = len(completed_bookings)
        total_cargo_handled_kg = sum(b.booked_capacity_kg for b in completed_bookings)

    # 6. Check compliance / KYC verification
    verified_doc = (
        db.query(provider_document)
        .filter(
            provider_document.provider_id == provider_id,
            provider_document.status == "VERIFIED"
        )
        .first()
    )
    compliance_verified = verified_doc is not None

    # 7. Return enriched provider details
    return {
        "provider_id": existing_provider.provider_id,
        "business_name": existing_provider.business_name,
        "business_address": existing_provider.business_address,
        "contact": existing_provider.contact,
        "email": existing_provider.user.email,
        "approval_status": existing_provider.approval_status,
        "created_at": getattr(existing_provider, "created_at", None),
        "active_containers_count": active_containers_count,
        "total_containers_count": total_containers_count,
        "completed_bookings_count": completed_bookings_count,
        "total_cargo_handled_kg": total_cargo_handled_kg,
        "serviced_routes": serviced_routes,
        "compliance_verified": compliance_verified,
    }