from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schemas.Provider.provider_registration_schema import (
    ProviderCreate,
    ProviderResponse
)

from app.schemas.Provider.search_provider_schema import (
    SearchResponse
    )

from app.schemas.Provider.provider_update_schema import (
    ProviderUpdate,
    ProviderUpdateResponse,
)

from app.schemas.Provider.provider_detail_schema import (
    ProviderDetailResponse
)

from app.controllers.Provider.provider_controller import (
    register_provider as register_provider_controller,
    search_provider as search_provider_controller,
    update_provider as update_provider_controller,
    get_provider_details as get_provider_details_controller,
)

from app.security.dependencies import get_current_user

router = APIRouter(
    prefix="/providers",
    tags=["Provider"]
)

@router.post("/", response_model=ProviderResponse)
def register_provider(
        provider: ProviderCreate,
        current_user = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return register_provider_controller(provider,current_user,db)

@router.get("/", response_model=list[SearchResponse])
def search_provider(

    business_name: str,
    db: Session = Depends(get_db)
):
    return search_provider_controller(business_name, db)

@router.put(
    "/{provider_id}",
    response_model=ProviderUpdateResponse
)
def update_provider(
    provider_id: int,
    provider: ProviderUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_provider_controller(
        provider_id,
        provider,
        current_user,
        db
    )

@router.get(
    "/{provider_id}",
    response_model=ProviderDetailResponse
)
def get_provider_details(
    provider_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_provider_details_controller(
        provider_id,
        current_user,
        db
    )