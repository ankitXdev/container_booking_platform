import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.security.dependencies import get_current_user


client = TestClient(app)

VALID_PAYLOAD = {
    "container_id": 1,
    "booked_capacity_kg": 500.0
}


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def create_mock_user(user_id=1, role="exporter"):
    class MockUser:
        pass

    user = MockUser()
    user.user_id = user_id
    user.role = role
    return user


# =========================================================
# SUCCESS
# =========================================================

def test_create_booking_route_success():

    mock_user = create_mock_user()
    app.dependency_overrides[get_current_user] = lambda: mock_user

    expected_response = {
        "message": "Booking created successfully",
        "booking_id": 1,
        "total_price": 1250.0,
        "status": "pending"
    }

    with patch(
        "app.routes.Booking.booking_router.create_booking_controller",
        return_value=expected_response
    ):
        response = client.post("/bookings/", json=VALID_PAYLOAD)

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Booking created successfully"
    assert data["booking_id"] == 1
    assert data["total_price"] == 1250.0
    assert data["status"] == "pending"

    app.dependency_overrides.clear()


# =========================================================
# MISSING FIELDS
# =========================================================

def test_create_booking_missing_container_id():

    mock_user = create_mock_user()
    app.dependency_overrides[get_current_user] = lambda: mock_user

    response = client.post("/bookings/", json={"booked_capacity_kg": 500.0})

    assert response.status_code == 422

    app.dependency_overrides.clear()


def test_create_booking_missing_capacity():

    mock_user = create_mock_user()
    app.dependency_overrides[get_current_user] = lambda: mock_user

    response = client.post("/bookings/", json={"container_id": 1})

    assert response.status_code == 422

    app.dependency_overrides.clear()


# =========================================================
# UNAUTHENTICATED
# =========================================================

def test_create_booking_requires_authentication():

    app.dependency_overrides.clear()

    response = client.post("/bookings/", json=VALID_PAYLOAD)

    assert response.status_code in [401, 403]


# =========================================================
# LIST BOOKINGS
# =========================================================

def test_list_bookings_route_success():

    mock_user = create_mock_user()
    app.dependency_overrides[get_current_user] = lambda: mock_user

    with patch(
        "app.routes.Booking.booking_router.list_bookings_controller",
        return_value=[]
    ):
        response = client.get("/bookings/")

    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()


def test_list_bookings_requires_authentication():

    app.dependency_overrides.clear()

    response = client.get("/bookings/")

    assert response.status_code in [401, 403]
