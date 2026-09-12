from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.booking_model import booking
from app.models.container_model import container
from app.models.provider_details_model import provider_details
from app.models.exporter_document_model import exporter_document


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ALLOWED_STATUSES = {"confirmed", "cancelled"}


def _get_booking_or_404(booking_id: int, db: Session):
    """Fetch a booking by ID or raise 404."""
    existing_booking = (
        db.query(booking)
        .filter(booking.booking_id == booking_id)
        .first()
    )

    if not existing_booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return existing_booking


def _get_provider_profile(current_user, db: Session):
    """Return provider profile for the current user, or None."""
    return (
        db.query(provider_details)
        .filter(provider_details.user_id == current_user.user_id)
        .first()
    )


# ---------------------------------------------------------------------------
# POST /bookings/
# ---------------------------------------------------------------------------

def create_booking(booking_data, current_user, db: Session):

    # 1. Only exporters can create bookings
    if current_user.role != "exporter":
        raise HTTPException(
            status_code=403,
            detail="Only exporters can create bookings"
        )

    # 2. Find the container
    existing_container = (
        db.query(container)
        .filter(container.container_id == booking_data.container_id)
        .first()
    )

    if not existing_container:
        raise HTTPException(
            status_code=404,
            detail="Container not found"
        )

    # 3. Container must be available
    if not existing_container.is_available:
        raise HTTPException(
            status_code=409,
            detail="Container is not available for booking"
        )

    # 4. Requested capacity must not exceed available capacity
    if booking_data.booked_capacity_kg > existing_container.available_capacity_kg:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Requested capacity ({booking_data.booked_capacity_kg} kg) "
                f"exceeds available capacity "
                f"({existing_container.available_capacity_kg} kg)"
            )
        )

    # 5. Exporter must have at least one VERIFIED document (compliance check)
    verified_doc = (
        db.query(exporter_document)
        .filter(
            exporter_document.user_id == current_user.user_id,
            exporter_document.status == "VERIFIED"
        )
        .first()
    )
    # If no verified doc found, check if there are any documents in db or if this is an unverified user
    if not verified_doc:
        any_doc = (
            db.query(exporter_document)
            .filter(exporter_document.user_id == current_user.user_id)
            .first()
        )
        if any_doc:
            raise HTTPException(
                status_code=403,
                detail="Your verification documents are pending admin approval or need revision."
            )
        else:
            raise HTTPException(
                status_code=403,
                detail="Account verification required: Please upload your business documents (IEC, GST, etc.) before booking container space."
            )

    # 5. Calculate total price
    total_price = round(
        booking_data.booked_capacity_kg * existing_container.price_per_kg,
        2
    )

    # 6. Create booking record
    new_booking = booking(
        container_id=booking_data.container_id,
        exporter_id=current_user.user_id,
        booked_capacity_kg=booking_data.booked_capacity_kg,
        total_price=total_price,
        status="pending"
    )

    # 7. Deduct booked capacity from the container
    existing_container.available_capacity_kg -= booking_data.booked_capacity_kg

    # 8. If no capacity left, mark container as unavailable
    if existing_container.available_capacity_kg <= 0:
        existing_container.is_available = False

    # 9. Save to database
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # 10. Return response
    return {
        "message": "Booking created successfully",
        "booking_id": new_booking.booking_id,
        "total_price": new_booking.total_price,
        "status": new_booking.status
    }


# ---------------------------------------------------------------------------
# GET /bookings/
# ---------------------------------------------------------------------------

def list_bookings(current_user, db: Session):

    # 1. Exporters see their own bookings
    if current_user.role == "exporter":
        bookings = (
            db.query(booking)
            .filter(booking.exporter_id == current_user.user_id)
            .order_by(booking.created_at.desc())
            .all()
        )

    # 2. Providers see bookings on their containers
    elif current_user.role == "provider":
        provider_profile = _get_provider_profile(current_user, db)

        if not provider_profile:
            raise HTTPException(
                status_code=403,
                detail="Provider profile not found. Please register as a provider first"
            )

        # Join booking → container → filter by provider_id
        bookings = (
            db.query(booking)
            .join(container, booking.container_id == container.container_id)
            .filter(container.provider_id == provider_profile.provider_id)
            .order_by(booking.created_at.desc())
            .all()
        )

    else:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    # 3. Build response list
    result = []

    for b in bookings:
        result.append({
            "booking_id": b.booking_id,
            "container_id": b.container_id,
            "exporter_id": b.exporter_id,
            "booked_capacity_kg": b.booked_capacity_kg,
            "total_price": b.total_price,
            "status": b.status,
            "origin": b.container.origin,
            "destination": b.container.destination,
            "departure_date": b.container.departure_date,
            "created_at": b.created_at
        })

    return result


# ---------------------------------------------------------------------------
# GET /bookings/{booking_id}
# ---------------------------------------------------------------------------

def get_booking_details(booking_id: int, current_user, db: Session):

    # 1. Find booking
    existing_booking = _get_booking_or_404(booking_id, db)

    # 2. Access control — only exporter who made it or provider who owns the container
    provider_profile = _get_provider_profile(current_user, db)

    is_exporter_owner = (
        existing_booking.exporter_id == current_user.user_id
    )
    is_container_provider = (
        provider_profile is not None
        and existing_booking.container.provider_id == provider_profile.provider_id
    )

    if not is_exporter_owner and not is_container_provider:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this booking"
        )

    # 3. Return full details
    c = existing_booking.container

    return {
        "booking_id": existing_booking.booking_id,
        "container_id": existing_booking.container_id,
        "exporter_id": existing_booking.exporter_id,
        "booked_capacity_kg": existing_booking.booked_capacity_kg,
        "total_price": existing_booking.total_price,
        "status": existing_booking.status,
        "created_at": existing_booking.created_at,
        "origin": c.origin,
        "destination": c.destination,
        "departure_date": c.departure_date,
        "price_per_kg": c.price_per_kg,
        "exporter_name": existing_booking.exporter.name,
        "exporter_email": existing_booking.exporter.email,
        "provider_business_name": c.provider.business_name,
        "provider_contact": c.provider.contact
    }


# ---------------------------------------------------------------------------
# PATCH /bookings/{booking_id}/status
# ---------------------------------------------------------------------------

def update_booking_status(
    booking_id: int,
    status_data,
    current_user,
    db: Session
):
    # 1. Only providers can update booking status
    if current_user.role != "provider":
        raise HTTPException(
            status_code=403,
            detail="Only providers can update booking status"
        )

    # 2. Validate new status value
    new_status = status_data.status.lower()

    if new_status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid status. Allowed values: {', '.join(ALLOWED_STATUSES)}"
        )

    # 3. Find booking
    existing_booking = _get_booking_or_404(booking_id, db)

    # 4. Ensure provider owns the container
    provider_profile = _get_provider_profile(current_user, db)

    if (
        not provider_profile
        or existing_booking.container.provider_id != provider_profile.provider_id
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to update this booking"
        )

    # 5. Cannot change status of an already cancelled booking
    if existing_booking.status == "cancelled":
        raise HTTPException(
            status_code=409,
            detail="Cannot update status of a cancelled booking"
        )

    # 6. Apply status change
    existing_booking.status = new_status

    # 7. Save changes
    db.commit()
    db.refresh(existing_booking)

    return {
        "message": "Booking status updated successfully",
        "status": existing_booking.status
    }


# ---------------------------------------------------------------------------
# POST /bookings/{booking_id}/cancel
# ---------------------------------------------------------------------------

def cancel_booking(booking_id: int, current_user, db: Session):

    # 1. Find booking
    existing_booking = _get_booking_or_404(booking_id, db)

    # 2. Access control — exporter who made it OR provider who owns the container
    provider_profile = _get_provider_profile(current_user, db)

    is_exporter_owner = (
        existing_booking.exporter_id == current_user.user_id
    )
    is_container_provider = (
        provider_profile is not None
        and existing_booking.container.provider_id == provider_profile.provider_id
    )

    if not is_exporter_owner and not is_container_provider:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to cancel this booking"
        )

    # 3. Already cancelled — nothing to do
    if existing_booking.status == "cancelled":
        raise HTTPException(
            status_code=409,
            detail="Booking is already cancelled"
        )

    # 4. Restore capacity to the container
    existing_booking.container.available_capacity_kg += (
        existing_booking.booked_capacity_kg
    )

    # 5. Re-enable container availability if it was marked unavailable
    if not existing_booking.container.is_available:
        existing_booking.container.is_available = True

    # 6. Mark booking as cancelled
    existing_booking.status = "cancelled"

    # 7. Save changes
    db.commit()
    db.refresh(existing_booking)

    return {
        "message": "Booking cancelled successfully",
        "booking_id": existing_booking.booking_id,
        "status": existing_booking.status
    }
