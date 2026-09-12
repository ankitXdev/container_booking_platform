import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime

from app.main import app
from app.security.dependencies import get_current_user


client = TestClient(app)


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


VALID_ORDER_PAYLOAD = {"booking_id": 1}

VALID_VERIFY_PAYLOAD = {
    "razorpay_order_id": "order_abc123",
    "razorpay_payment_id": "pay_xyz789",
    "razorpay_signature": "valid_signature_string"
}


# =========================================================
# CREATE ORDER - SUCCESS
# =========================================================

def test_create_payment_order_route_success():

    app.dependency_overrides[get_current_user] = lambda: create_mock_user()

    expected_response = {
        "razorpay_order_id": "order_abc123",
        "amount": 1250.0,
        "amount_in_paise": 125000,
        "currency": "INR",
        "booking_id": 1,
        "key_id": "rzp_test_xxx"
    }

    with patch(
        "app.routes.Payment.payment_router.create_payment_order_controller",
        return_value=expected_response
    ):
        response = client.post("/payments/create-order", json=VALID_ORDER_PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    assert data["razorpay_order_id"] == "order_abc123"
    assert data["amount"] == 1250.0
    assert data["currency"] == "INR"

    app.dependency_overrides.clear()


# =========================================================
# CREATE ORDER - MISSING BOOKING ID
# =========================================================

def test_create_payment_order_missing_booking_id():

    app.dependency_overrides[get_current_user] = lambda: create_mock_user()

    response = client.post("/payments/create-order", json={})

    assert response.status_code == 422

    app.dependency_overrides.clear()


# =========================================================
# CREATE ORDER - NO AUTH
# =========================================================

def test_create_payment_order_requires_auth():

    app.dependency_overrides.clear()

    response = client.post("/payments/create-order", json=VALID_ORDER_PAYLOAD)

    assert response.status_code in [401, 403]


# =========================================================
# VERIFY PAYMENT - SUCCESS
# =========================================================

def test_verify_payment_route_success():

    app.dependency_overrides[get_current_user] = lambda: create_mock_user()

    expected_response = {
        "message": "Payment verified successfully",
        "booking_id": 1,
        "payment_id": 1,
        "status": "paid"
    }

    with patch(
        "app.routes.Payment.payment_router.verify_payment_controller",
        return_value=expected_response
    ):
        response = client.post("/payments/verify", json=VALID_VERIFY_PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paid"
    assert data["message"] == "Payment verified successfully"

    app.dependency_overrides.clear()


# =========================================================
# VERIFY PAYMENT - MISSING FIELDS
# =========================================================

def test_verify_payment_missing_signature():

    app.dependency_overrides[get_current_user] = lambda: create_mock_user()

    incomplete_payload = {
        "razorpay_order_id": "order_abc123",
        "razorpay_payment_id": "pay_xyz789"
        # missing razorpay_signature
    }

    response = client.post("/payments/verify", json=incomplete_payload)

    assert response.status_code == 422

    app.dependency_overrides.clear()


# =========================================================
# VERIFY PAYMENT - NO AUTH
# =========================================================

def test_verify_payment_requires_auth():

    app.dependency_overrides.clear()

    response = client.post("/payments/verify", json=VALID_VERIFY_PAYLOAD)

    assert response.status_code in [401, 403]


# =========================================================
# GET PAYMENT DETAILS - SUCCESS
# =========================================================

def test_get_payment_details_route_success():

    app.dependency_overrides[get_current_user] = lambda: create_mock_user()

    expected_response = {
        "payment_id": 1,
        "booking_id": 1,
        "razorpay_order_id": "order_abc123",
        "razorpay_payment_id": "pay_xyz789",
        "amount": 1250.0,
        "currency": "INR",
        "status": "paid",
        "created_at": "2025-12-01T10:00:00",
        "origin": "Mumbai",
        "destination": "Dubai",
        "booked_capacity_kg": 500.0,
        "total_price": 1250.0,
        "booking_status": "confirmed"
    }

    with patch(
        "app.routes.Payment.payment_router.get_payment_details_controller",
        return_value=expected_response
    ):
        response = client.get("/payments/1")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paid"
    assert data["origin"] == "Mumbai"

    app.dependency_overrides.clear()


# =========================================================
# GET PAYMENT DETAILS - NO AUTH
# =========================================================

def test_get_payment_details_requires_auth():

    app.dependency_overrides.clear()

    response = client.get("/payments/1")

    assert response.status_code in [401, 403]
