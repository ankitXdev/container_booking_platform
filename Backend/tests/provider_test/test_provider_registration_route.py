import pytest

from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.security.dependencies import get_current_user


client = TestClient(app)


# =========================================================
# HELPER
# =========================================================

def create_mock_user(
    user_id=1,
    role="provider"
):
    class MockUser:
        pass

    user = MockUser()
    user.user_id = user_id
    user.role = role

    return user


# =========================================================
# SUCCESS
# =========================================================

def test_provider_registration_success():

    mock_user = create_mock_user(
        user_id=999999,
        role="provider"
    )

    app.dependency_overrides[get_current_user] = (
        lambda: mock_user
    )

    payload = {
        "business_name": "ABC Logistics",
        "business_address": "Mumbai, Maharashtra",
        "contact": "9876543210"
    }

    expected_response = {
        "message": "Provider registration successful",
        "provider_id": 999,
        "approval_status": "pending"
    }

    with patch(
        "app.routes.Provider.provider_router.register_provider_controller",
        return_value=expected_response
    ):

        response = client.post(
            "/providers/",
            json=payload
        )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Provider registration successful"
    assert data["provider_id"] == 999
    assert data["approval_status"] == "pending"

    app.dependency_overrides.clear()


# =========================================================
# WRONG ROLE
# =========================================================

def test_provider_registration_wrong_role():

    mock_user = create_mock_user(
        user_id=1,
        role="exporter"
    )

    app.dependency_overrides[get_current_user] = (
        lambda: mock_user
    )

    payload = {
        "business_name": "ABC Logistics",
        "business_address": "Mumbai, Maharashtra",
        "contact": "9876543210"
    }

    response = client.post(
        "/providers/",
        json=payload
    )

    assert response.status_code == 403

    assert response.json()["detail"] == (
        "Only users with provider role can register as a provider"
    )

    app.dependency_overrides.clear()


# =========================================================
# MISSING BUSINESS NAME
# =========================================================

def test_provider_registration_missing_business_name():

    mock_user = create_mock_user()

    app.dependency_overrides[get_current_user] = (
        lambda: mock_user
    )

    payload = {
        "business_address": "Mumbai, Maharashtra",
        "contact": "9876543210"
    }

    response = client.post(
        "/providers/",
        json=payload
    )

    assert response.status_code == 422

    app.dependency_overrides.clear()


# =========================================================
# MISSING BUSINESS ADDRESS
# =========================================================

def test_provider_registration_missing_address():

    mock_user = create_mock_user()

    app.dependency_overrides[get_current_user] = (
        lambda: mock_user
    )

    payload = {
        "business_name": "ABC Logistics",
        "contact": "9876543210"
    }

    response = client.post(
        "/providers/",
        json=payload
    )

    assert response.status_code == 422

    app.dependency_overrides.clear()


# =========================================================
# MISSING CONTACT
# =========================================================

def test_provider_registration_missing_contact():

    mock_user = create_mock_user()

    app.dependency_overrides[get_current_user] = (
        lambda: mock_user
    )

    payload = {
        "business_name": "ABC Logistics",
        "business_address": "Mumbai, Maharashtra"
    }

    response = client.post(
        "/providers/",
        json=payload
    )

    assert response.status_code == 422

    app.dependency_overrides.clear()


# =========================================================
# WITHOUT AUTHENTICATION
# =========================================================

def test_provider_registration_without_authentication():

    # Make sure there is no dependency override
    app.dependency_overrides.clear()

    payload = {
        "business_name": "ABC Logistics",
        "business_address": "Mumbai, Maharashtra",
        "contact": "9876543210"
    }

    response = client.post(
        "/providers/",
        json=payload
    )

    assert response.status_code in [401, 403]