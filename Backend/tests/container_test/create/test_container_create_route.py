import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.security.dependencies import get_current_user


client = TestClient(app)


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def create_mock_user(user_id=1, role="provider"):
    class MockUser:
        pass

    user = MockUser()
    user.user_id = user_id
    user.role = role
    return user


VALID_PAYLOAD = {
    "origin": "Mumbai",
    "destination": "Dubai",
    "departure_date": "2025-12-01T10:00:00",
    "total_capacity_kg": 5000.0,
    "available_capacity_kg": 3000.0,
    "price_per_kg": 2.5
}


# =========================================================
# SUCCESS
# =========================================================

def test_create_container_route_success():

    mock_user = create_mock_user()
    app.dependency_overrides[get_current_user] = lambda: mock_user

    expected_response = {
        "message": "Container listing created successfully",
        "container_id": 1
    }

    with patch(
        "app.routes.Container.container_router.create_container_controller",
        return_value=expected_response
    ):
        response = client.post("/containers/", json=VALID_PAYLOAD)

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Container listing created successfully"
    assert data["container_id"] == 1

    app.dependency_overrides.clear()


# =========================================================
# MISSING REQUIRED FIELD
# =========================================================

def test_create_container_missing_origin():

    mock_user = create_mock_user()
    app.dependency_overrides[get_current_user] = lambda: mock_user

    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "origin"}

    response = client.post("/containers/", json=payload)

    assert response.status_code == 422

    app.dependency_overrides.clear()


def test_create_container_missing_destination():

    mock_user = create_mock_user()
    app.dependency_overrides[get_current_user] = lambda: mock_user

    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "destination"}

    response = client.post("/containers/", json=payload)

    assert response.status_code == 422

    app.dependency_overrides.clear()


def test_create_container_missing_departure_date():

    mock_user = create_mock_user()
    app.dependency_overrides[get_current_user] = lambda: mock_user

    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "departure_date"}

    response = client.post("/containers/", json=payload)

    assert response.status_code == 422

    app.dependency_overrides.clear()


# =========================================================
# WITHOUT AUTHENTICATION
# =========================================================

def test_create_container_without_authentication():

    app.dependency_overrides.clear()

    response = client.post("/containers/", json=VALID_PAYLOAD)

    assert response.status_code in [401, 403]


# =========================================================
# WRONG HTTP METHOD
# =========================================================

def test_create_container_wrong_method():

    response = client.get("/containers/")

    # GET /containers/ is a valid route (search), not 405
    # POST /containers/ is the create — test that DELETE is not allowed
    response = client.delete("/containers/")

    assert response.status_code in [405, 422]
