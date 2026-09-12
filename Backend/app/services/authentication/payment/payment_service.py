import hmac
import hashlib

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.booking_model import booking
from app.models.payment_model import payment
from app.models.provider_details_model import provider_details
from app.config.razorpay_config import get_razorpay_client, RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_booking_or_404(booking_id: int, db: Session):
    """Fetch a booking by ID or raise 404."""
    existing_booking = (
        db.query(booking)
        .filter(booking.booking_id == booking_id)
        .first()
    )

    if not existing_booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return existing_booking


def _get_provider_profile(current_user, db: Session):
    """Return provider profile for the current user, or None."""
    return (
        db.query(provider_details)
        .filter(provider_details.user_id == current_user.user_id)
        .first()
    )


# ---------------------------------------------------------------------------
# POST /payments/create-order
# ---------------------------------------------------------------------------

def create_payment_order(order_data, current_user, db: Session):

    # 1. Only exporters create payment orders
    if current_user.role != "exporter":
        raise HTTPException(
            status_code=403,
            detail="Only exporters can initiate payments"
        )

    # 2. Find the booking
    existing_booking = _get_booking_or_404(order_data.booking_id, db)

    # 3. Must be the exporter who made the booking
    if existing_booking.exporter_id != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to pay for this booking"
        )

    # 4. Booking must be in pending status to be paid
    if existing_booking.status != "pending":
        raise HTTPException(
            status_code=409,
            detail=f"Cannot initiate payment for a booking with status: {existing_booking.status}"
        )

    # 5. Check if a payment order already exists for this booking
    existing_payment = (
        db.query(payment)
        .filter(payment.booking_id == order_data.booking_id)
        .first()
    )

    if existing_payment and existing_payment.status == "paid":
        raise HTTPException(
            status_code=409,
            detail="Payment for this booking is already completed"
        )

    # 6. Create Razorpay order
    client = get_razorpay_client()

    amount_in_paise = int(existing_booking.total_price * 100)   # Razorpay uses paise

    razorpay_order = client.order.create({
        "amount": amount_in_paise,
        "currency": "INR",
        "receipt": f"booking_{existing_booking.booking_id}",
        "payment_capture": 1   # auto-capture after payment
    })

    # 7. Save or update payment record in DB
    if existing_payment:
        # Replace previous failed/created order with a new one
        existing_payment.razorpay_order_id = razorpay_order["id"]
        existing_payment.amount = existing_booking.total_price
        existing_payment.status = "created"
        existing_payment.razorpay_payment_id = None
        existing_payment.razorpay_signature = None
    else:
        new_payment = payment(
            booking_id=existing_booking.booking_id,
            razorpay_order_id=razorpay_order["id"],
            amount=existing_booking.total_price,
            currency="INR",
            status="created"
        )
        db.add(new_payment)

    db.commit()

    # 8. Return order details including public key for frontend checkout
    return {
        "razorpay_order_id": razorpay_order["id"],
        "amount": existing_booking.total_price,
        "amount_in_paise": amount_in_paise,
        "currency": "INR",
        "booking_id": existing_booking.booking_id,
        "key_id": RAZORPAY_KEY_ID
    }


# ---------------------------------------------------------------------------
# POST /payments/verify
# ---------------------------------------------------------------------------

def verify_payment(verify_data, current_user, db: Session):

    # 1. Only exporters verify their own payment
    if current_user.role != "exporter":
        raise HTTPException(
            status_code=403,
            detail="Only exporters can verify payments"
        )

    # 2. Find the payment record by razorpay_order_id
    existing_payment = (
        db.query(payment)
        .filter(
            payment.razorpay_order_id == verify_data.razorpay_order_id
        )
        .first()
    )

    if not existing_payment:
        raise HTTPException(
            status_code=404,
            detail="Payment order not found"
        )

    # 3. Must belong to the current user's booking
    existing_booking = _get_booking_or_404(
        existing_payment.booking_id, db
    )

    if existing_booking.exporter_id != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to verify this payment"
        )

    # 4. Already verified — idempotent
    if existing_payment.status == "paid":
        return {
            "message": "Payment already verified",
            "booking_id": existing_booking.booking_id,
            "payment_id": existing_payment.payment_id,
            "status": existing_payment.status
        }

    # 5. Verify HMAC SHA256 signature
    #    Razorpay signature = HMAC(order_id + "|" + payment_id, key_secret)
    expected_signature = hmac.new(
        RAZORPAY_KEY_SECRET.encode("utf-8"),
        f"{verify_data.razorpay_order_id}|{verify_data.razorpay_payment_id}".encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    if expected_signature != verify_data.razorpay_signature:
        # 6a. Signature mismatch — mark payment as failed
        existing_payment.status = "failed"
        db.commit()

        raise HTTPException(
            status_code=400,
            detail="Payment verification failed: invalid signature"
        )

    # 6b. Signature valid — mark payment as paid
    existing_payment.razorpay_payment_id = verify_data.razorpay_payment_id
    existing_payment.razorpay_signature = verify_data.razorpay_signature
    existing_payment.status = "paid"

    # 7. Confirm the booking
    existing_booking.status = "confirmed"

    db.commit()
    db.refresh(existing_payment)

    return {
        "message": "Payment verified successfully",
        "booking_id": existing_booking.booking_id,
        "payment_id": existing_payment.payment_id,
        "status": existing_payment.status
    }


# ---------------------------------------------------------------------------
# GET /payments/{booking_id}
# ---------------------------------------------------------------------------

def get_payment_details(booking_id: int, current_user, db: Session):

    # 1. Find the booking
    existing_booking = _get_booking_or_404(booking_id, db)

    # 2. Access control — exporter who owns booking or the container's provider
    provider_profile = _get_provider_profile(current_user, db)

    is_exporter_owner = (
        existing_booking.exporter_id == current_user.user_id
    )
    is_container_provider = (
        provider_profile is not None
        and existing_booking.container.provider_id == provider_profile.provider_id
    )

    if not is_exporter_owner and not is_container_provider:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this payment"
        )

    # 3. Find the payment record
    existing_payment = (
        db.query(payment)
        .filter(payment.booking_id == booking_id)
        .first()
    )

    if not existing_payment:
        raise HTTPException(
            status_code=404,
            detail="No payment found for this booking"
        )

    # 4. Return payment + booking summary
    c = existing_booking.container

    return {
        "payment_id": existing_payment.payment_id,
        "booking_id": existing_payment.booking_id,
        "razorpay_order_id": existing_payment.razorpay_order_id,
        "razorpay_payment_id": existing_payment.razorpay_payment_id,
        "amount": existing_payment.amount,
        "currency": existing_payment.currency,
        "status": existing_payment.status,
        "created_at": existing_payment.created_at,
        "origin": c.origin,
        "destination": c.destination,
        "booked_capacity_kg": existing_booking.booked_capacity_kg,
        "total_price": existing_booking.total_price,
        "booking_status": existing_booking.status
    }
