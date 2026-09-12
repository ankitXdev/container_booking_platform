from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.security.dependencies import get_current_user

from app.schemas.Payment.payment_create_order_schema import (
    CreateOrderRequest,
    CreateOrderResponse,
)
from app.schemas.Payment.payment_verify_schema import (
    VerifyPaymentRequest,
    VerifyPaymentResponse,
)
from app.schemas.Payment.payment_detail_schema import PaymentDetailResponse

from app.controllers.Payment.payment_controller import (
    create_payment_order as create_payment_order_controller,
    verify_payment as verify_payment_controller,
    get_payment_details as get_payment_details_controller,
)

# Main code starts from here

router = APIRouter(
    prefix="/payments",
    tags=["Payment"]
)


@router.post(
    "/create-order",
    response_model=CreateOrderResponse
)
def create_payment_order(
    order_data: CreateOrderRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_payment_order_controller(order_data, current_user, db)


@router.post(
    "/verify",
    response_model=VerifyPaymentResponse
)
def verify_payment(
    verify_data: VerifyPaymentRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return verify_payment_controller(verify_data, current_user, db)


@router.get(
    "/{booking_id}",
    response_model=PaymentDetailResponse
)
def get_payment_details(
    booking_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_payment_details_controller(booking_id, current_user, db)
