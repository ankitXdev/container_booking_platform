import pytest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.config.database import get_db


# =========================================================
# TEST DATABASE
# =========================================================

def override_get_db():
    db = MagicMock()
    yield db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# =========================================================
# REGISTER
# =========================================================

def test_register_success():

    mock_user = MagicMock()

    mock_user.user_id = 1
    mock_user.name = "Ankit"
    mock_user.email = "ankit@example.com"
    mock_user.role = "exporter"
    mock_user.status = "active"

    request_data = {
        "name": "Ankit",
        "email": "ankit@example.com",
        "password": "verysecurepassword123",
        "role": "exporter",
        "status": "active"
    }

    with patch(
        "app.routes.Authentication.auth_router.register_user_controller",
        return_value=mock_user
    ) as mock_register:

        response = client.post(
            "/auth/register",
            json=request_data
        )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == 1
    assert data["name"] == "Ankit"
    assert data["email"] == "ankit@example.com"
    assert data["role"] == "exporter"
    assert data["status"] == "active"

    mock_register.assert_called_once()


# =========================================================
# REGISTER - INVALID DATA
# =========================================================

def test_register_invalid_email():

    request_data = {
        "name": "Ankit",
        "email": "not-an-email",
        "password": "verysecurepassword123",
        "role": "exporter",
        "status": "active"
    }

    response = client.post(
        "/auth/register",
        json=request_data
    )

    assert response.status_code == 422


def test_register_password_too_short():

    request_data = {
        "name": "Ankit",
        "email": "ankit@example.com",
        "password": "short",
        "role": "exporter",
        "status": "active"
    }

    response = client.post(
        "/auth/register",
        json=request_data
    )

    assert response.status_code == 422


def test_register_missing_field():

    request_data = {
        "name": "Ankit",
        "email": "ankit@example.com",
        "password": "verysecurepassword123",
        "role": "exporter"
    }

    response = client.post(
        "/auth/register",
        json=request_data
    )

    assert response.status_code == 422


# =========================================================
# LOGIN
# =========================================================

def test_login_success():

    mock_user = MagicMock()

    mock_user.name = "Ankit"

    request_data = {
        "email": "ankit@example.com",
        "password": "verysecurepassword123"
    }

    mock_token = "fake_access_token"

    with patch(
        "app.routes.Authentication.auth_router.login_user_controller",
        return_value={
            "message": "Login successful",
            "name": "Ankit",
            "access_token": mock_token,
            "token_type": "bearer"
        }
    ) as mock_login:

        response = client.post(
            "/auth/login",
            json=request_data
        )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Login successful"
    assert data["name"] == "Ankit"
    assert data["access_token"] == mock_token
    assert data["token_type"] == "bearer"

    mock_login.assert_called_once()


def test_login_invalid_email_format():

    request_data = {
        "email": "invalid-email",
        "password": "verysecurepassword123"
    }

    response = client.post(
        "/auth/login",
        json=request_data
    )

    assert response.status_code == 422


def test_login_missing_password():

    request_data = {
        "email": "ankit@example.com"
    }

    response = client.post(
        "/auth/login",
        json=request_data
    )

    assert response.status_code == 422


# =========================================================
# LOGOUT
# =========================================================

def test_logout_success():

    response = client.post("/auth/logout")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Logout successful"


# =========================================================
# WRONG HTTP METHODS / ROUTES
# =========================================================

def test_register_wrong_method():

    response = client.get("/auth/register")

    assert response.status_code == 405


def test_login_wrong_method():

    response = client.get("/auth/login")

    assert response.status_code == 405