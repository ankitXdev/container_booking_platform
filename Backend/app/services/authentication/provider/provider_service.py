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

    return {
    "message": "Provider registration successful",
    "status": "pending"
    }

