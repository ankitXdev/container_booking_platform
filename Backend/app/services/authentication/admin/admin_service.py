from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user_model import users
from app.models.provider_details_model import provider_details
from app.models.container_model import container
from app.models.booking_model import booking


# ---------------------------------------------------------------------------
# Helper — admin-only guard
# ---------------------------------------------------------------------------

def _require_admin(current_user):
    """Raise 403 if the caller is not an admin."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )


# ---------------------------------------------------------------------------
# GET /admin/providers/pending
# ---------------------------------------------------------------------------

def get_pending_providers(current_user, db: Session):

    # 1. Admin only
    _require_admin(current_user)

    # 2. Fetch all providers whose approval_status is "pending"
    pending = (
        db.query(provider_details)
        .filter(provider_details.approval_status == "pending")
        .order_by(provider_details.created_at.asc())
        .all()
    )

    # 3. Build response
    result = []

    for p in pending:
        result.append({
            "provider_id": p.provider_id,
            "user_id": p.user_id,
            "business_name": p.business_name,
            "business_address": p.business_address,
            "contact": p.contact,
            "approval_status": p.approval_status,
            "email": p.user.email
        })

    return result


# ---------------------------------------------------------------------------
# PATCH /admin/providers/{provider_id}/approve
# ---------------------------------------------------------------------------

def approve_provider(provider_id: int, current_user, db: Session):

    # 1. Admin only
    _require_admin(current_user)

    # 2. Find the provider
    existing_provider = (
        db.query(provider_details)
        .filter(provider_details.provider_id == provider_id)
        .first()
    )

    if not existing_provider:
        raise HTTPException(
            status_code=404,
            detail="Provider not found"
        )

    # 3. Already approved — idempotent, no error
    if existing_provider.approval_status == "approved":
        return {
            "message": "Provider is already approved",
            "provider_id": existing_provider.provider_id,
            "approval_status": existing_provider.approval_status
        }

    # 4. Approve
    existing_provider.approval_status = "approved"

    db.commit()
    db.refresh(existing_provider)

    return {
        "message": "Provider approved successfully",
        "provider_id": existing_provider.provider_id,
        "approval_status": existing_provider.approval_status
    }


# ---------------------------------------------------------------------------
# PATCH /admin/providers/{provider_id}/reject
# ---------------------------------------------------------------------------

def reject_provider(provider_id: int, current_user, db: Session):

    # 1. Admin only
    _require_admin(current_user)

    # 2. Find the provider
    existing_provider = (
        db.query(provider_details)
        .filter(provider_details.provider_id == provider_id)
        .first()
    )

    if not existing_provider:
        raise HTTPException(
            status_code=404,
            detail="Provider not found"
        )

    # 3. Already rejected — idempotent
    if existing_provider.approval_status == "rejected":
        return {
            "message": "Provider is already rejected",
            "provider_id": existing_provider.provider_id,
            "approval_status": existing_provider.approval_status
        }

    # 4. Reject
    existing_provider.approval_status = "rejected"

    db.commit()
    db.refresh(existing_provider)

    return {
        "message": "Provider rejected successfully",
        "provider_id": existing_provider.provider_id,
        "approval_status": existing_provider.approval_status
    }


# ---------------------------------------------------------------------------
# GET /admin/stats
# ---------------------------------------------------------------------------

def get_platform_stats(current_user, db: Session):

    # 1. Admin only
    _require_admin(current_user)

    # 2. User counts
    total_users = db.query(func.count(users.user_id)).scalar()

    total_exporters = (
        db.query(func.count(users.user_id))
        .filter(users.role == "exporter")
        .scalar()
    )

    total_providers_users = (
        db.query(func.count(users.user_id))
        .filter(users.role == "provider")
        .scalar()
    )

    # 3. Provider approval breakdown
    total_providers = db.query(func.count(provider_details.provider_id)).scalar()

    pending_providers = (
        db.query(func.count(provider_details.provider_id))
        .filter(provider_details.approval_status == "pending")
        .scalar()
    )

    approved_providers = (
        db.query(func.count(provider_details.provider_id))
        .filter(provider_details.approval_status == "approved")
        .scalar()
    )

    rejected_providers = (
        db.query(func.count(provider_details.provider_id))
        .filter(provider_details.approval_status == "rejected")
        .scalar()
    )

    # 4. Container breakdown
    total_containers = db.query(func.count(container.container_id)).scalar()

    available_containers = (
        db.query(func.count(container.container_id))
        .filter(container.is_available == True)
        .scalar()
    )

    # 5. Booking breakdown
    total_bookings = db.query(func.count(booking.booking_id)).scalar()

    pending_bookings = (
        db.query(func.count(booking.booking_id))
        .filter(booking.status == "pending")
        .scalar()
    )

    confirmed_bookings = (
        db.query(func.count(booking.booking_id))
        .filter(booking.status == "confirmed")
        .scalar()
    )

    cancelled_bookings = (
        db.query(func.count(booking.booking_id))
        .filter(booking.status == "cancelled")
        .scalar()
    )

    # 6. Total revenue — sum of confirmed bookings
    total_revenue = (
        db.query(func.sum(booking.total_price))
        .filter(booking.status == "confirmed")
        .scalar()
        or 0.0
    )

    return {
        "total_users": total_users,
        "total_exporters": total_exporters,
        "total_providers": total_providers_users,
        "providers": {
            "total": total_providers,
            "pending": pending_providers,
            "approved": approved_providers,
            "rejected": rejected_providers
        },
        "containers": {
            "total": total_containers,
            "available": available_containers,
            "unavailable": total_containers - available_containers
        },
        "bookings": {
            "total": total_bookings,
            "pending": pending_bookings,
            "confirmed": confirmed_bookings,
            "cancelled": cancelled_bookings
        },
        "total_revenue": round(total_revenue, 2)
    }


# ---------------------------------------------------------------------------
# GET /admin/bookings
# ---------------------------------------------------------------------------

def get_all_bookings(current_user, db: Session):

    # 1. Admin only
    _require_admin(current_user)

    # 2. Fetch all bookings, most recent first
    all_bookings = (
        db.query(booking)
        .order_by(booking.created_at.desc())
        .all()
    )

    # 3. Build detailed response list
    result = []

    for b in all_bookings:
        result.append({
            "booking_id": b.booking_id,
            "container_id": b.container_id,
            "exporter_id": b.exporter_id,
            "exporter_name": b.exporter.name,
            "exporter_email": b.exporter.email,
            "provider_business_name": b.container.provider.business_name,
            "origin": b.container.origin,
            "destination": b.container.destination,
            "booked_capacity_kg": b.booked_capacity_kg,
            "total_price": b.total_price,
            "status": b.status,
            "created_at": b.created_at
        })

    return result
