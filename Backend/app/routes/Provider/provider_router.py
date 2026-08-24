from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schemas.Provider.provider_schema import (
    ProviderCreate,
    ProviderResponse
)

from app.controllers.Provider.provider_controller import register_provider_service as register_provider_controller

from app.security.dependencies import get_current_user

router = APIRouter(
    prefix="/providers",
    tags=["Provider"]
)

@router.post("/providers", response_model=ProviderResponse)
def register_provider(
        provider: ProviderCreate,
        current_user = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return register_provider_controller(provider,current_user,db)