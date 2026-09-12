from sqlalchemy.orm import Session

from app.services.authentication.booking.booking_service import (
    create_booking as create_booking_service,
    list_bookings as list_bookings_service,
    get_booking_details as get_booking_details_service,
    update_booking_status as update_booking_status_service,
    cancel_booking as cancel_booking_service,
)


def create_booking(booking_data, current_user, db: Session):
    return create_booking_service(booking_data, current_user, db)


def list_bookings(current_user, db: Session):
    return list_bookings_service(current_user, db)


def get_booking_details(booking_id: int, current_user, db: Session):
    return get_booking_details_service(booking_id, current_user, db)


def update_booking_status(
    booking_id: int,
    status_data,
    current_user,
    db: Session
):
    return update_booking_status_service(
        booking_id,
        status_data,
        current_user,
        db
    )


def cancel_booking(booking_id: int, current_user, db: Session):
    return cancel_booking_service(booking_id, current_user, db)
