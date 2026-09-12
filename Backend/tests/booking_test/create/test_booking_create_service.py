import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from app.services.authentication.booking.booking_service import (
    create_booking
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def create_mock_user(user_id=1, role="exporter"):
    user = MagicMock()
    user.user_id = user_id
    user.role = role
    return user


def create_mock_booking_data(container_id=1, booked_capacity_kg=500.0):
    data = MagicMock()
    data.container_id = container_id
    data.booked_capacity_kg = booked_capacity_kg
    return data


def create_mock_container(
    container_id=1,
    is_available=True,
    available_capacity_kg=3000.0,
    price_per_kg=2.5
):
    c = MagicMock()
    c.container_id = container_id
    c.is_available = is_available
    c.available_capacity_kg = available_capacity_kg
    c.price_per_kg = price_per_kg
    return c


# =========================================================
# CREATE BOOKING - SUCCESS
# =========================================================

def test_create_booking_success():

    current_user = create_mock_user(role="exporter")
    db = MagicMock()

    mock_container = create_mock_container()

    # First query → container, second call is not needed
    db.query.return_value.filter.return_value.first.return_value = mock_container

    with patch(
        "app.services.authentication.booking.booking_service.booking"
    ) as mock_booking_model:

        new_booking = MagicMock()
        new_booking.booking_id = 1
        new_booking.total_price = 1250.0
        new_booking.status = "pending"
        mock_booking_model.return_value = new_booking

        result = create_booking(create_mock_booking_data(), current_user, db)

    db.add.assert_called_once_with(new_booking)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_booking)

    assert result["message"] == "Booking created successfully"
    assert result["booking_id"] == 1
    assert result["status"] == "pending"


# =========================================================
# CREATE BOOKING - WRONG ROLE
# =========================================================

def test_create_booking_only_exporters_allowed():

    current_user = create_mock_user(role="provider")
    db = MagicMock()

    with pytest.raises(HTTPException) as exc_info:
        create_booking(create_mock_booking_data(), current_user, db)

    assert exc_info.value.status_code == 403
    assert "Only exporters" in exc_info.value.detail

    db.add.assert_not_called()
    db.commit.assert_not_called()


# =========================================================
# CREATE BOOKING - CONTAINER NOT FOUND
# =========================================================

def test_create_booking_container_not_found():

    current_user = create_mock_user()
    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        create_booking(create_mock_booking_data(), current_user, db)

    assert exc_info.value.status_code == 404
    assert "Container not found" in exc_info.value.detail


# =========================================================
# CREATE BOOKING - CONTAINER UNAVAILABLE
# =========================================================

def test_create_booking_container_not_available():

    current_user = create_mock_user()
    db = MagicMock()

    mock_container = create_mock_container(is_available=False)
    db.query.return_value.filter.return_value.first.return_value = mock_container

    with pytest.raises(HTTPException) as exc_info:
        create_booking(create_mock_booking_data(), current_user, db)

    assert exc_info.value.status_code == 409
    assert "not available" in exc_info.value.detail


# =========================================================
# CREATE BOOKING - CAPACITY EXCEEDED
# =========================================================

def test_create_booking_capacity_exceeded():

    current_user = create_mock_user()
    db = MagicMock()

    # Container has only 200 kg available, booking requests 500 kg
    mock_container = create_mock_container(available_capacity_kg=200.0)
    db.query.return_value.filter.return_value.first.return_value = mock_container

    booking_data = create_mock_booking_data(booked_capacity_kg=500.0)

    with pytest.raises(HTTPException) as exc_info:
        create_booking(booking_data, current_user, db)

    assert exc_info.value.status_code == 422
    assert "exceeds available capacity" in exc_info.value.detail


# =========================================================
# CREATE BOOKING - PRICE CALCULATION
# =========================================================

def test_create_booking_total_price_calculated_correctly():

    current_user = create_mock_user()
    db = MagicMock()

    # 500 kg × ₹2.5/kg = ₹1250
    mock_container = create_mock_container(
        available_capacity_kg=3000.0,
        price_per_kg=2.5
    )
    db.query.return_value.filter.return_value.first.return_value = mock_container

    with patch(
        "app.services.authentication.booking.booking_service.booking"
    ) as mock_booking_model:

        new_booking = MagicMock()
        new_booking.booking_id = 1
        new_booking.total_price = 1250.0
        new_booking.status = "pending"
        mock_booking_model.return_value = new_booking

        booking_data = create_mock_booking_data(booked_capacity_kg=500.0)
        result = create_booking(booking_data, current_user, db)

    # Verify the model was called — price should be 500 * 2.5 = 1250
    call_kwargs = mock_booking_model.call_args.kwargs
    assert call_kwargs["total_price"] == 1250.0


# =========================================================
# CREATE BOOKING - CAPACITY DEDUCTED FROM CONTAINER
# =========================================================

def test_create_booking_deducts_container_capacity():

    current_user = create_mock_user()
    db = MagicMock()

    mock_container = create_mock_container(available_capacity_kg=3000.0)
    db.query.return_value.filter.return_value.first.return_value = mock_container

    with patch(
        "app.services.authentication.booking.booking_service.booking"
    ) as mock_booking_model:

        new_booking = MagicMock()
        new_booking.booking_id = 1
        new_booking.total_price = 1250.0
        new_booking.status = "pending"
        mock_booking_model.return_value = new_booking

        booking_data = create_mock_booking_data(booked_capacity_kg=500.0)
        create_booking(booking_data, current_user, db)

    # 3000 - 500 = 2500 remaining
    assert mock_container.available_capacity_kg == 2500.0
