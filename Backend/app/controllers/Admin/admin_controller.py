from sqlalchemy.orm import Session

from app.services.authentication.admin.admin_service import (
    get_pending_providers as get_pending_providers_service,
    approve_provider as approve_provider_service,
    reject_provider as reject_provider_service,
    get_platform_stats as get_platform_stats_service,
    get_all_bookings as get_all_bookings_service,
)


def get_pending_providers(current_user, db: Session):
    return get_pending_providers_service(current_user, db)


def approve_provider(provider_id: int, current_user, db: Session):
    return approve_provider_service(provider_id, current_user, db)


def reject_provider(provider_id: int, current_user, db: Session):
    return reject_provider_service(provider_id, current_user, db)


def get_platform_stats(current_user, db: Session):
    return get_platform_stats_service(current_user, db)


def get_all_bookings(current_user, db: Session):
    return get_all_bookings_service(current_user, db)
