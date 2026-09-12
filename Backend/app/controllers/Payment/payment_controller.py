from sqlalchemy.orm import Session

from app.services.authentication.payment.payment_service import (
    create_payment_order as create_payment_order_service,
    verify_payment as verify_payment_service,
    get_payment_details as get_payment_details_service,
)


def create_payment_order(order_data, current_user, db: Session):
    return create_payment_order_service(order_data, current_user, db)


def verify_payment(verify_data, current_user, db: Session):
    return verify_payment_service(verify_data, current_user, db)


def get_payment_details(booking_id: int, current_user, db: Session):
    return get_payment_details_service(booking_id, current_user, db)
