from sqlalchemy.orm import Session

from app.schemas.Provider.provider_schema import ProviderCreate

from app.services.authentication.provider.provider_service import register_provider as register_provider_service

def register_provider(provider:ProviderCreate , db: Session):

    return register_provider_service(provider, db)