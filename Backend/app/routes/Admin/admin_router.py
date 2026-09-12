from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.security.dependencies import get_current_user

from app.schemas.Admin.admin_pending_providers_schema import PendingProviderItem
from app.schemas.Admin.admin_provider_approval_schema import ProviderApprovalResponse
from app.schemas.Admin.admin_stats_schema import PlatformStatsResponse
from app.schemas.Admin.admin_bookings_schema import AdminBookingItem

from app.controllers.Admin.admin_controller import (
    get_pending_providers as get_pending_providers_controller,
    approve_provider as approve_provider_controller,
    reject_provider as reject_provider_controller,
    get_platform_stats as get_platform_stats_controller,
    get_all_bookings as get_all_bookings_controller,
)

# Main code starts from here

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get(
    "/providers/pending",
    response_model=list[PendingProviderItem]
)
def get_pending_providers(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_pending_providers_controller(current_user, db)


@router.patch(
    "/providers/{provider_id}/approve",
    response_model=ProviderApprovalResponse
)
def approve_provider(
    provider_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return approve_provider_controller(provider_id, current_user, db)


@router.patch(
    "/providers/{provider_id}/reject",
    response_model=ProviderApprovalResponse
)
def reject_provider(
    provider_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return reject_provider_controller(provider_id, current_user, db)


@router.get(
    "/stats",
    response_model=PlatformStatsResponse
)
def get_platform_stats(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_platform_stats_controller(current_user, db)


@router.get(
    "/bookings",
    response_model=list[AdminBookingItem]
)
def get_all_bookings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_all_bookings_controller(current_user, db)
