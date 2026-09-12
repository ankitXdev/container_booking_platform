import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.services.authentication.booking.booking_service import (
    cancel_booking,
    update_booking_status
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
    status="pending",
    booked_capacity_kg=500.0
):
    b = MagicMock()
    b.booking_id = booking_id
    b.exporter_id = exporter_id
    b.status = status
    b.booked_capacity_kg = booked_capacity_kg
    b.container = MagicMock()
    b.container.provider_id = provider_id
    b.container.is_available = True
    b.container.available_capacity_kg = 2500.0
    return b


def create_mock_provider(provider_id=1, user_id=1):
    p = MagicMock()
    p.provider_id = provider_id
    p.user_id = user_id
    return p


# =========================================================
# CANCEL BOOKING - SUCCESS (exporter)
# =========================================================

def test_cancel_booking_success_by_exporter():

    current_user = create_mock_user(user_id=1, role="exporter")
    db = MagicMock()

    mock_booking = create_mock_booking(exporter_id=1, status="pending")

    # First query → booking, second → no provider profile (user is exporter)
    db.query.return_value.filter.return_value.first.side_effect = [
        mock_booking,
        None        # no provider profile for exporter
    ]

    result = cancel_booking(booking_id=1, current_user=current_user, db=db)

    db.commit.assert_called_once()
    assert mock_booking.status == "cancelled"
    assert result["message"] == "Booking cancelled successfully"
    assert result["status"] == "cancelled"


# =========================================================
# CANCEL BOOKING - ALREADY CANCELLED
# =========================================================

def test_cancel_booking_already_cancelled():

    current_user = create_mock_user()
    db = MagicMock()

    mock_booking = create_mock_booking(status="cancelled")
    db.query.return_value.filter.return_value.first.side_effect = [
        mock_booking,
        None
    ]

    with pytest.raises(HTTPException) as exc_info:
        cancel_booking(booking_id=1, current_user=current_user, db=db)

    assert exc_info.value.status_code == 409
    assert "already cancelled" in exc_info.value.detail

    db.commit.assert_not_called()


# =========================================================
# CANCEL BOOKING - NOT FOUND
# =========================================================

def test_cancel_booking_not_found():

    current_user = create_mock_user()
    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        cancel_booking(booking_id=999, current_user=current_user, db=db)

    assert exc_info.value.status_code == 404
    assert "Booking not found" in exc_info.value.detail


# =========================================================
# CANCEL BOOKING - CAPACITY RESTORED
# =========================================================

def test_cancel_booking_restores_container_capacity():

    current_user = create_mock_user(user_id=1)
    db = MagicMock()

    mock_booking = create_mock_booking(
        exporter_id=1,
        status="pending",
        booked_capacity_kg=500.0
    )
    mock_booking.container.available_capacity_kg = 2500.0

    db.query.return_value.filter.return_value.first.side_effect = [
        mock_booking,
        None
    ]

    cancel_booking(booking_id=1, current_user=current_user, db=db)

    # 2500 + 500 = 3000
    assert mock_booking.container.available_capacity_kg == 3000.0


# =========================================================
# UPDATE STATUS - SUCCESS (provider)
# =========================================================

def test_update_booking_status_success():

    current_user = create_mock_user(user_id=2, role="provider")
    db = MagicMock()

    mock_booking = create_mock_booking(provider_id=10, status="pending")
    mock_provider = create_mock_provider(provider_id=10, user_id=2)

    # Service call order:
    # 1. _get_booking_or_404 → booking
    # 2. _get_provider_profile → provider profile
    db.query.return_value.filter.return_value.first.side_effect = [
        mock_booking,   # _get_booking_or_404
        mock_provider   # _get_provider_profile
    ]

    status_data = MagicMock()
    status_data.status = "confirmed"

    result = update_booking_status(
        booking_id=1,
        status_data=status_data,
        current_user=current_user,
        db=db
    )

    assert result["message"] == "Booking status updated successfully"


# =========================================================
# UPDATE STATUS - WRONG ROLE
# =========================================================

def test_update_booking_status_exporters_cannot_update():

    current_user = create_mock_user(role="exporter")
    db = MagicMock()

    status_data = MagicMock()
    status_data.status = "confirmed"

    with pytest.raises(HTTPException) as exc_info:
        update_booking_status(
            booking_id=1,
            status_data=status_data,
            current_user=current_user,
            db=db
        )

    assert exc_info.value.status_code == 403
    assert "Only providers" in exc_info.value.detail


# =========================================================
# UPDATE STATUS - INVALID VALUE
# =========================================================

def test_update_booking_status_invalid_value():

    current_user = create_mock_user(role="provider")
    db = MagicMock()

    status_data = MagicMock()
    status_data.status = "shipped"   # not a valid status

    with pytest.raises(HTTPException) as exc_info:
        update_booking_status(
            booking_id=1,
            status_data=status_data,
            current_user=current_user,
            db=db
        )

    assert exc_info.value.status_code == 422
    assert "Invalid status" in exc_info.value.detail
