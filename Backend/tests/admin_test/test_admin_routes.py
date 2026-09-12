import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.security.dependencies import get_current_user


client = TestClient(app)


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def create_mock_user(role="admin"):
    class MockUser:
        pass

    user = MockUser()
    user.user_id = 1
    user.role = role
    return user


# =========================================================
# GET PENDING PROVIDERS - SUCCESS
# =========================================================

def test_get_pending_providers_route_success():

    app.dependency_overrides[get_current_user] = lambda: create_mock_user(role="admin")

    expected_response = [
        {
            "provider_id": 1,
            "user_id": 1,
            "business_name": "ABC Logistics",
            "business_address": "Mumbai",
            "contact": "9876543210",
            "approval_status": "pending",
            "email": "abc@example.com"
        }
    ]

    with patch(
        "app.routes.Admin.admin_router.get_pending_providers_controller",
        return_value=expected_response
    ):
        response = client.get("/admin/providers/pending")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["approval_status"] == "pending"

    app.dependency_overrides.clear()


# =========================================================
# GET PENDING PROVIDERS - NO AUTH
# =========================================================

def test_get_pending_providers_requires_auth():

    app.dependency_overrides.clear()

    response = client.get("/admin/providers/pending")

    assert response.status_code in [401, 403]


# =========================================================
# APPROVE PROVIDER - SUCCESS
# =========================================================

def test_approve_provider_route_success():

    app.dependency_overrides[get_current_user] = lambda: create_mock_user(role="admin")

    expected_response = {
        "message": "Provider approved successfully",
        "provider_id": 1,
        "approval_status": "approved"
    }

    with patch(
        "app.routes.Admin.admin_router.approve_provider_controller",
        return_value=expected_response
    ):
        response = client.patch("/admin/providers/1/approve")

    assert response.status_code == 200
    data = response.json()
    assert data["approval_status"] == "approved"

    app.dependency_overrides.clear()


# =========================================================
# REJECT PROVIDER - SUCCESS
# =========================================================

def test_reject_provider_route_success():

    app.dependency_overrides[get_current_user] = lambda: create_mock_user(role="admin")

    expected_response = {
        "message": "Provider rejected successfully",
        "provider_id": 1,
        "approval_status": "rejected"
    }

    with patch(
        "app.routes.Admin.admin_router.reject_provider_controller",
        return_value=expected_response
    ):
        response = client.patch("/admin/providers/1/reject")

    assert response.status_code == 200
    data = response.json()
    assert data["approval_status"] == "rejected"

    app.dependency_overrides.clear()


# =========================================================
# GET STATS - SUCCESS
# =========================================================

def test_get_platform_stats_route_success():

    app.dependency_overrides[get_current_user] = lambda: create_mock_user(role="admin")

    expected_response = {
        "total_users": 50,
        "total_exporters": 30,
        "total_providers": 15,
        "providers": {
            "total": 15,
            "pending": 3,
            "approved": 10,
            "rejected": 2
        },
        "containers": {
            "total": 20,
            "available": 15,
            "unavailable": 5
        },
        "bookings": {
            "total": 40,
            "pending": 10,
            "confirmed": 25,
            "cancelled": 5
        },
        "total_revenue": 250000.0
    }

    with patch(
        "app.routes.Admin.admin_router.get_platform_stats_controller",
        return_value=expected_response
    ):
        response = client.get("/admin/stats")

    assert response.status_code == 200
    data = response.json()
    assert data["total_users"] == 50
    assert data["total_revenue"] == 250000.0
    assert data["providers"]["pending"] == 3

    app.dependency_overrides.clear()


# =========================================================
# GET ALL BOOKINGS - SUCCESS
# =========================================================

def test_get_all_bookings_route_success():

    app.dependency_overrides[get_current_user] = lambda: create_mock_user(role="admin")

    with patch(
        "app.routes.Admin.admin_router.get_all_bookings_controller",
        return_value=[]
    ):
        response = client.get("/admin/bookings")

    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()
