from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.security.dependencies import get_current_user

from app.schemas.Booking.booking_create_schema import (
    BookingCreate,
    BookingCreateResponse,
)
from app.schemas.Booking.booking_list_schema import BookingListItem
from app.schemas.Booking.booking_detail_schema import BookingDetailResponse
from app.schemas.Booking.booking_status_schema import (
    BookingStatusUpdate,
    BookingStatusResponse,
)
from app.schemas.Booking.booking_cancel_schema import BookingCancelResponse

from app.controllers.Booking.booking_controller import (
    create_booking as create_booking_controller,
    list_bookings as list_bookings_controller,
    get_booking_details as get_booking_details_controller,
    update_booking_status as update_booking_status_controller,
    cancel_booking as cancel_booking_controller,
)

# Main code starts from here

router = APIRouter(
    prefix="/bookings",
    tags=["Booking"]
)


@router.post("/", response_model=BookingCreateResponse)
def create_booking(
    booking_data: BookingCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_booking_controller(booking_data, current_user, db)


@router.get("/", response_model=list[BookingListItem])
def list_bookings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return list_bookings_controller(current_user, db)


@router.get("/{booking_id}", response_model=BookingDetailResponse)
def get_booking_details(
    booking_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_booking_details_controller(booking_id, current_user, db)


@router.patch(
    "/{booking_id}/status",
    response_model=BookingStatusResponse
)
def update_booking_status(
    booking_id: int,
    status_data: BookingStatusUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_booking_status_controller(
        booking_id,
        status_data,
        current_user,
        db
    )


@router.post(
    "/{booking_id}/cancel",
    response_model=BookingCancelResponse
)
def cancel_booking(
    booking_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return cancel_booking_controller(booking_id, current_user, db)
