import pytest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.security.dependencies import get_current_user


client = TestClient(app)


@pytest.fixture(autouse=True)
def override_current_user():

    class MockUser:
        user_id = 1
        role = "exporter"

    app.dependency_overrides[get_current_user] = lambda: MockUser()

    yield

    app.dependency_overrides.clear()


def test_get_provider_details_success():

    mock_response = {
        "provider_id": 15,
        "business_name": "ABC Logistics",
        "business_address": "Mumbai, Maharashtra",
        "contact": "9876543210",
        "email": "abc@example.com",
        "approval_status": "approved"
    }

    with patch(
        "app.routes.Provider.provider_router.get_provider_details_controller",
        return_value=mock_response
    ) as mock_controller:

        response = client.get("/providers/15")

    assert response.status_code == 200

    data = response.json()

    assert data["provider_id"] == 15
    assert data["business_name"] == "ABC Logistics"
    assert data["business_address"] == "Mumbai, Maharashtra"
    assert data["contact"] == "9876543210"
    assert data["email"] == "abc@example.com"
    assert data["approval_status"] == "approved"

    mock_controller.assert_called_once()


def test_get_provider_details_requires_authentication():

    app.dependency_overrides.clear()

    response = client.get("/providers/15")

    assert response.status_code == 401