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
        role = "provider"

    app.dependency_overrides[get_current_user] = lambda: MockUser()

    yield

    app.dependency_overrides.clear()


def test_update_provider_success():
    mock_response = {
        "message": "Provider profile updated successfully"
    }

    with patch(
        "app.routes.Provider.provider_router.update_provider_controller",
        return_value=mock_response
    ) as mock_controller:

        response = client.put(
            "/providers/1",
            json={
                "business_name": "Updated Agro Services",
                "business_address": "Lucknow, Uttar Pradesh",
                "contact": "9876543210"
            }
        )

    assert response.status_code == 200
    assert response.json() == mock_response
    mock_controller.assert_called_once()


def test_update_provider_requires_business_name():
    response = client.put(
        "/providers/1",
        json={
            "business_address": "Lucknow, Uttar Pradesh",
            "contact": "9876543210"
        }
    )

    assert response.status_code == 422


def test_update_provider_requires_business_address():
    response = client.put(
        "/providers/1",
        json={
            "business_name": "Updated Agro Services",
            "contact": "9876543210"
        }
    )

    assert response.status_code == 422


def test_update_provider_requires_contact():
    response = client.put(
        "/providers/1",
        json={
            "business_name": "Updated Agro Services",
            "business_address": "Lucknow, Uttar Pradesh"
        }
    )

    assert response.status_code == 422


def test_update_provider_rejects_invalid_contact():
    response = client.put(
        "/providers/1",
        json={
            "business_name": "Updated Agro Services",
            "business_address": "Lucknow, Uttar Pradesh",
            "contact": "123"
        }
    )

    assert response.status_code == 422