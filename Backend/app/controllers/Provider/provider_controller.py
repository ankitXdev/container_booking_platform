from sqlalchemy.orm import Session

from app.schemas.Provider.provider_registration_schema import ProviderCreate
from app.schemas.Provider.search_provider_schema import ProviderSearch

from app.services.authentication.provider.provider_service import (
    register_provider as register_provider_service,
    search_provider as search_provider_service,
    update_provider as update_provider_service,
)

def register_provider(
    provider: ProviderCreate,
    current_user,
    db: Session
):
    return register_provider_service(
        provider,
        current_user,
        db
    )

def search_provider(provider:ProviderSearch, db:Session):

    return search_provider_service(provider,db)

def update_provider(
    provider_id: int,
    provider,
    current_user,
    db: Session
):
    return update_provider_service(
        provider_id,
        provider,
        current_user,
        db
    )