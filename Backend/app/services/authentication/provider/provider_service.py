from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.provider_details_model import provider_details


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