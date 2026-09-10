from sqlalchemy.orm import Session

from app.services.authentication.container.container_service import (
    create_container as create_container_service,
    search_containers as search_containers_service,
    get_container_details as get_container_details_service,
    update_container as update_container_service,
    delete_container as delete_container_service,
    update_container_availability as update_container_availability_service,
)


def create_container(container_data, current_user, db: Session):
    return create_container_service(container_data, current_user, db)


def search_containers(
    origin,
    destination,
    min_capacity_kg,
    db: Session
):
    return search_containers_service(origin, destination, min_capacity_kg, db)


def get_container_details(container_id: int, db: Session):
    return get_container_details_service(container_id, db)


def update_container(
    container_id: int,
    container_data,
    current_user,
    db: Session
):
    return update_container_service(
        container_id,
        container_data,
        current_user,
        db
    )


def delete_container(container_id: int, current_user, db: Session):
    return delete_container_service(container_id, current_user, db)


def update_container_availability(
    container_id: int,
    availability_data,
    current_user,
    db: Session
):
    return update_container_availability_service(
        container_id,
        availability_data,
        current_user,
        db
    )
