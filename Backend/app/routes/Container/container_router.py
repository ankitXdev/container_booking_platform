from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.security.dependencies import get_current_user

from app.schemas.Container.container_create_schema import (
    ContainerCreate,
    ContainerCreateResponse,
)
from app.schemas.Container.container_search_schema import ContainerSearchResponse
from app.schemas.Container.container_detail_schema import ContainerDetailResponse
from app.schemas.Container.container_update_schema import (
    ContainerUpdate,
    ContainerUpdateResponse,
)
from app.schemas.Container.container_delete_schema import ContainerDeleteResponse
from app.schemas.Container.container_availability_schema import (
    ContainerAvailabilityUpdate,
    ContainerAvailabilityResponse,
)

from app.controllers.Container.container_controller import (
    create_container as create_container_controller,
    search_containers as search_containers_controller,
    get_container_details as get_container_details_controller,
    update_container as update_container_controller,
    delete_container as delete_container_controller,
    update_container_availability as update_container_availability_controller,
)

# Main code starts from here

router = APIRouter(
    prefix="/containers",
    tags=["Container"]
)


@router.post("/", response_model=ContainerCreateResponse)
def create_container(
    container_data: ContainerCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_container_controller(container_data, current_user, db)


@router.get("/", response_model=list[ContainerSearchResponse])
def search_containers(
    origin: str | None = None,
    destination: str | None = None,
    min_capacity_kg: float | None = None,
    provider_id: int | None = None,
    db: Session = Depends(get_db)
):
    return search_containers_controller(origin, destination, min_capacity_kg, db, provider_id)


@router.get("/{container_id}", response_model=ContainerDetailResponse)
def get_container_details(
    container_id: int,
    db: Session = Depends(get_db)
):
    return get_container_details_controller(container_id, db)


@router.put("/{container_id}", response_model=ContainerUpdateResponse)
def update_container(
    container_id: int,
    container_data: ContainerUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_container_controller(
        container_id,
        container_data,
        current_user,
        db
    )


@router.delete("/{container_id}", response_model=ContainerDeleteResponse)
def delete_container(
    container_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_container_controller(container_id, current_user, db)


@router.patch(
    "/{container_id}/availability",
    response_model=ContainerAvailabilityResponse
)
def update_container_availability(
    container_id: int,
    availability_data: ContainerAvailabilityUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_container_availability_controller(
        container_id,
        availability_data,
        current_user,
        db
    )
