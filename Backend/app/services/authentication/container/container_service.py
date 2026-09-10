from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.container_model import container
from app.models.provider_details_model import provider_details


# ---------------------------------------------------------------------------
# Helper — get the caller's provider profile or raise 403
# ---------------------------------------------------------------------------

def _get_approved_provider(current_user, db: Session):
    """
    Resolves the provider profile for the current user.
    Raises 403 if the user is not a provider or not yet approved.
    """
    if current_user.role != "provider":
        raise HTTPException(
            status_code=403,
            detail="Only providers can manage containers"
        )

    provider_profile = (
        db.query(provider_details)
        .filter(provider_details.user_id == current_user.user_id)
        .first()
    )

    if not provider_profile:
        raise HTTPException(
            status_code=403,
            detail="Provider profile not found. Please register as a provider first"
        )

    if provider_profile.approval_status != "approved":
        raise HTTPException(
            status_code=403,
            detail="Your provider account is pending admin approval"
        )

    return provider_profile


# ---------------------------------------------------------------------------
# POST /containers/
# ---------------------------------------------------------------------------

def create_container(container_data, current_user, db: Session):

    # 1. Caller must be an approved provider
    provider_profile = _get_approved_provider(current_user, db)

    # 2. Validate capacity
    if container_data.available_capacity_kg > container_data.total_capacity_kg:
        raise HTTPException(
            status_code=422,
            detail="available_capacity_kg cannot exceed total_capacity_kg"
        )

    # 3. Create container record
    new_container = container(
        provider_id=provider_profile.provider_id,
        origin=container_data.origin,
        destination=container_data.destination,
        departure_date=container_data.departure_date,
        total_capacity_kg=container_data.total_capacity_kg,
        available_capacity_kg=container_data.available_capacity_kg,
        price_per_kg=container_data.price_per_kg,
        is_available=True
    )

    # 4. Save to database
    db.add(new_container)
    db.commit()
    db.refresh(new_container)

    # 5. Return response
    return {
        "message": "Container listing created successfully",
        "container_id": new_container.container_id
    }


# ---------------------------------------------------------------------------
# GET /containers/
# ---------------------------------------------------------------------------

def search_containers(
    origin: str | None,
    destination: str | None,
    min_capacity_kg: float | None,
    db: Session
):
    query = (
        db.query(container)
        .filter(container.is_available == True)
    )

    # Apply optional filters
    if origin:
        query = query.filter(
            container.origin.ilike(f"%{origin.strip()}%")
        )

    if destination:
        query = query.filter(
            container.destination.ilike(f"%{destination.strip()}%")
        )

    if min_capacity_kg is not None:
        query = query.filter(
            container.available_capacity_kg >= min_capacity_kg
        )

    containers = query.all()

    result = []

    for c in containers:
        result.append({
            "container_id": c.container_id,
            "provider_id": c.provider_id,
            "origin": c.origin,
            "destination": c.destination,
            "departure_date": c.departure_date,
            "total_capacity_kg": c.total_capacity_kg,
            "available_capacity_kg": c.available_capacity_kg,
            "price_per_kg": c.price_per_kg,
            "is_available": c.is_available
        })

    return result


# ---------------------------------------------------------------------------
# GET /containers/{container_id}
# ---------------------------------------------------------------------------

def get_container_details(container_id: int, db: Session):

    # 1. Find the container
    existing_container = (
        db.query(container)
        .filter(container.container_id == container_id)
        .first()
    )

    # 2. Container does not exist
    if not existing_container:
        raise HTTPException(
            status_code=404,
            detail="Container not found"
        )

    # 3. Return container details with provider info
    return {
        "container_id": existing_container.container_id,
        "provider_id": existing_container.provider_id,
        "origin": existing_container.origin,
        "destination": existing_container.destination,
        "departure_date": existing_container.departure_date,
        "total_capacity_kg": existing_container.total_capacity_kg,
        "available_capacity_kg": existing_container.available_capacity_kg,
        "price_per_kg": existing_container.price_per_kg,
        "is_available": existing_container.is_available,
        "provider_business_name": existing_container.provider.business_name,
        "provider_contact": existing_container.provider.contact
    }


# ---------------------------------------------------------------------------
# PUT /containers/{container_id}
# ---------------------------------------------------------------------------

def update_container(
    container_id: int,
    container_data,
    current_user,
    db: Session
):
    # 1. Find the container
    existing_container = (
        db.query(container)
        .filter(container.container_id == container_id)
        .first()
    )

    if not existing_container:
        raise HTTPException(
            status_code=404,
            detail="Container not found"
        )

    # 2. Only the owning provider can update
    provider_profile = (
        db.query(provider_details)
        .filter(provider_details.user_id == current_user.user_id)
        .first()
    )

    if (
        not provider_profile
        or existing_container.provider_id != provider_profile.provider_id
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to update this container"
        )

    # 3. Validate capacity
    if container_data.available_capacity_kg > container_data.total_capacity_kg:
        raise HTTPException(
            status_code=422,
            detail="available_capacity_kg cannot exceed total_capacity_kg"
        )

    # 4. Apply updates
    existing_container.origin = container_data.origin
    existing_container.destination = container_data.destination
    existing_container.departure_date = container_data.departure_date
    existing_container.total_capacity_kg = container_data.total_capacity_kg
    existing_container.available_capacity_kg = container_data.available_capacity_kg
    existing_container.price_per_kg = container_data.price_per_kg

    # 5. Save changes
    db.commit()
    db.refresh(existing_container)

    return {
        "message": "Container updated successfully"
    }


# ---------------------------------------------------------------------------
# DELETE /containers/{container_id}
# ---------------------------------------------------------------------------

def delete_container(container_id: int, current_user, db: Session):

    # 1. Find the container
    existing_container = (
        db.query(container)
        .filter(container.container_id == container_id)
        .first()
    )

    if not existing_container:
        raise HTTPException(
            status_code=404,
            detail="Container not found"
        )

    # 2. Only the owning provider can delete
    provider_profile = (
        db.query(provider_details)
        .filter(provider_details.user_id == current_user.user_id)
        .first()
    )

    if (
        not provider_profile
        or existing_container.provider_id != provider_profile.provider_id
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to delete this container"
        )

    # 3. Delete record
    db.delete(existing_container)
    db.commit()

    return {
        "message": "Container deleted successfully"
    }


# ---------------------------------------------------------------------------
# PATCH /containers/{container_id}/availability
# ---------------------------------------------------------------------------

def update_container_availability(
    container_id: int,
    availability_data,
    current_user,
    db: Session
):
    # 1. Find the container
    existing_container = (
        db.query(container)
        .filter(container.container_id == container_id)
        .first()
    )

    if not existing_container:
        raise HTTPException(
            status_code=404,
            detail="Container not found"
        )

    # 2. Only the owning provider can toggle availability
    provider_profile = (
        db.query(provider_details)
        .filter(provider_details.user_id == current_user.user_id)
        .first()
    )

    if (
        not provider_profile
        or existing_container.provider_id != provider_profile.provider_id
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to update this container"
        )

    # 3. Apply availability change
    existing_container.is_available = availability_data.is_available

    # 4. Save changes
    db.commit()
    db.refresh(existing_container)

    return {
        "message": "Container availability updated successfully",
        "is_available": existing_container.is_available
    }
