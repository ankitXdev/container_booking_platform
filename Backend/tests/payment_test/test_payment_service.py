import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from app.services.authentication.payment.payment_service import (
    create_payment_order,
    verify_payment,
    get_payment_details
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def create_mock_user(user_id=1, role="exporter"):
    user = MagicMock()
    user.user_id = user_id
    user.role = role
    return user


def create_mock_booking(
    booking_id=1,
    exporter_id=1,
    provider_id=1,
    total_price=1250.0,
    status="pending"
):
    b = MagicMock()
    b.booking_id = booking_id
    b.exporter_id = exporter_id
    b.total_price = total_price
    b.status = status
    b.container = MagicMock()
    b.container.provider_id = provider_id
    b.container.origin = "Mumbai"
    b.container.destination = "Dubai"
    return b


def create_mock_payment(
    payment_id=1,
    booking_id=1,
    razorpay_order_id="order_123",
    status="created"
):
    p = MagicMock()
    p.payment_id = payment_id
    p.booking_id = booking_id
    p.razorpay_order_id = razorpay_order_id
    p.razorpay_payment_id = None
    p.razorpay_signature = None
    p.amount = 1250.0
    p.currency = "INR"
    p.status = status
    return p


# =========================================================
# CREATE PAYMENT ORDER - SUCCESS
# =========================================================

def test_create_payment_order_success():

    current_user = create_mock_user(role="exporter")
    db = MagicMock()

    order_data = MagicMock()
    order_data.booking_id = 1

    mock_booking = create_mock_booking(exporter_id=1, status="pending")

    # booking query → booking, payment query → None (no existing payment)
    db.query.return_value.filter.return_value.first.side_effect = [
        mock_booking,
        None
    ]

    mock_razorpay_order = {"id": "order_abc123"}

    with patch(
        "app.services.authentication.payment.payment_service.get_razorpay_client"
    ) as mock_client_factory, patch(
        "app.services.authentication.payment.payment_service.payment"
    ) as mock_payment_model:

        mock_client = MagicMock()
        mock_client.order.create.return_value = mock_razorpay_order
        mock_client_factory.return_value = mock_client

        new_payment = MagicMock()
        mock_payment_model.return_value = new_payment

        result = create_payment_order(order_data, current_user, db)

    assert result["razorpay_order_id"] == "order_abc123"
    assert result["amount"] == 1250.0
    assert result["currency"] == "INR"
    assert result["booking_id"] == 1

    db.add.assert_called_once_with(new_payment)
    db.commit.assert_called_once()


# =========================================================
# CREATE PAYMENT ORDER - WRONG ROLE
# =========================================================

def test_create_payment_order_only_exporters():

    current_user = create_mock_user(role="provider")
    db = MagicMock()

    order_data = MagicMock()
    order_data.booking_id = 1

    with pytest.raises(HTTPException) as exc_info:
        create_payment_order(order_data, current_user, db)

    assert exc_info.value.status_code == 403
    assert "Only exporters" in exc_info.value.detail

    db.add.assert_not_called()


# =========================================================
# CREATE PAYMENT ORDER - BOOKING NOT FOUND
# =========================================================

def test_create_payment_order_booking_not_found():

    current_user = create_mock_user()
    db = MagicMock()

    order_data = MagicMock()
    order_data.booking_id = 999

    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        create_payment_order(order_data, current_user, db)

    assert exc_info.value.status_code == 404
    assert "Booking not found" in exc_info.value.detail


# =========================================================
# CREATE PAYMENT ORDER - BOOKING NOT PENDING
# =========================================================

def test_create_payment_order_booking_not_pending():

    current_user = create_mock_user()
    db = MagicMock()

    order_data = MagicMock()
    order_data.booking_id = 1

    mock_booking = create_mock_booking(exporter_id=1, status="confirmed")
    db.query.return_value.filter.return_value.first.side_effect = [
        mock_booking,
        None
    ]

    with pytest.raises(HTTPException) as exc_info:
        create_payment_order(order_data, current_user, db)

    assert exc_info.value.status_code == 409
    assert "Cannot initiate payment" in exc_info.value.detail


# =========================================================
# CREATE PAYMENT ORDER - UNAUTHORIZED EXPORTER
# =========================================================

def test_create_payment_order_unauthorized_exporter():

    current_user = create_mock_user(user_id=99, role="exporter")
    db = MagicMock()

    order_data = MagicMock()
    order_data.booking_id = 1

    # Booking belongs to exporter_id=1, but current user is 99
    mock_booking = create_mock_booking(exporter_id=1, status="pending")
    db.query.return_value.filter.return_value.first.side_effect = [
        mock_booking,
        None
    ]

    with pytest.raises(HTTPException) as exc_info:
        create_payment_order(order_data, current_user, db)

    assert exc_info.value.status_code == 403
    assert "not authorized" in exc_info.value.detail


# =========================================================
# VERIFY PAYMENT - INVALID SIGNATURE
# =========================================================

def test_verify_payment_invalid_signature():

    current_user = create_mock_user()
    db = MagicMock()

    verify_data = MagicMock()
    verify_data.razorpay_order_id = "order_123"
    verify_data.razorpay_payment_id = "pay_abc"
    verify_data.razorpay_signature = "bad_signature"

    mock_payment_rec = create_mock_payment(status="created")
    mock_booking = create_mock_booking(exporter_id=1, status="pending")

    db.query.return_value.filter.return_value.first.side_effect = [
        mock_payment_rec,
        mock_booking
    ]

    with patch(
        "app.services.authentication.payment.payment_service.RAZORPAY_KEY_SECRET",
        "test_secret"
    ):
        with pytest.raises(HTTPException) as exc_info:
            verify_payment(verify_data, current_user, db)

    assert exc_info.value.status_code == 400
    assert "invalid signature" in exc_info.value.detail

    # Payment should be marked failed
    assert mock_payment_rec.status == "failed"


# =========================================================
# VERIFY PAYMENT - PAYMENT NOT FOUND
# =========================================================

def test_verify_payment_order_not_found():

    current_user = create_mock_user()
    db = MagicMock()

    verify_data = MagicMock()
    verify_data.razorpay_order_id = "order_nonexistent"
    verify_data.razorpay_payment_id = "pay_abc"
    verify_data.razorpay_signature = "sig"

    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        verify_payment(verify_data, current_user, db)

    assert exc_info.value.status_code == 404
    assert "Payment order not found" in exc_info.value.detail


# =========================================================
# GET PAYMENT DETAILS - SUCCESS
# =========================================================

def test_get_payment_details_success():

    current_user = create_mock_user(user_id=1)
    db = MagicMock()

    mock_booking = create_mock_booking(exporter_id=1, status="confirmed")
    mock_booking.booked_capacity_kg = 500.0
    mock_booking.container.origin = "Mumbai"
    mock_booking.container.destination = "Dubai"
    mock_booking.container.price_per_kg = 2.5

    mock_payment_rec = create_mock_payment(status="paid")
    mock_payment_rec.created_at = __import__("datetime").datetime(2025, 12, 1, 10, 0, 0)

    # First query → booking, second → no provider, third → payment
    db.query.return_value.filter.return_value.first.side_effect = [
        mock_booking,
        None,              # no provider profile (user is exporter)
        mock_payment_rec
    ]

    result = get_payment_details(booking_id=1, current_user=current_user, db=db)

    assert result["payment_id"] == 1
    assert result["status"] == "paid"
    assert result["origin"] == "Mumbai"
    assert result["destination"] == "Dubai"


# =========================================================
# GET PAYMENT DETAILS - NO PAYMENT RECORD
# =========================================================

def test_get_payment_details_no_payment_yet():

    current_user = create_mock_user(user_id=1)
    db = MagicMock()

    mock_booking = create_mock_booking(exporter_id=1, status="pending")

    db.query.return_value.filter.return_value.first.side_effect = [
        mock_booking,
        None,    # no provider profile
        None     # no payment record
    ]

    with pytest.raises(HTTPException) as exc_info:
        get_payment_details(booking_id=1, current_user=current_user, db=db)

    assert exc_info.value.status_code == 404
    assert "No payment found" in exc_info.value.detail
