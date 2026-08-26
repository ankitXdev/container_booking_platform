from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_search_provider_returns_multiple_providers():
    # Arrange
    mock_providers = [
        {
            "provider_id": 1,
            "business_name": "Sharma Agro Services",
            "business_address": "Lucknow",
            "contact": "9876543210",
            "email": "sharma1@example.com"
        },
        {
            "provider_id": 2,
            "business_name": "Sharma Agro Services",
            "business_address": "Kanpur",
            "contact": "9123456780",
            "email": "sharma2@example.com"
        }
    ]

    with patch(
        "app.routes.Provider.provider_router.search_provider_controller",
        return_value=mock_providers
    ):
        # Act
        response = client.get(
            "/providers/",
            params={"business_name": "Sharma"}
        )

    # Assert
    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0] == {
        "provider_id": 1,
        "business_name": "Sharma Agro Services",
        "business_address": "Lucknow",
        "contact": "9876543210",
        "email": "sharma1@example.com"
    }

    assert data[1] == {
        "provider_id": 2,
        "business_name": "Sharma Agro Services",
        "business_address": "Kanpur",
        "contact": "9123456780",
        "email": "sharma2@example.com"
    }


def test_search_provider_returns_empty_list():
    # Arrange
    with patch(
        "app.routes.Provider.provider_router.search_provider_controller",
        return_value=[]
    ):
        # Act
        response = client.get(
            "/providers/",
            params={"business_name": "NonExistingBusiness"}
        )

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_search_provider_requires_business_name():
    # Act
    response = client.get("/providers/")

    # Assert
    assert response.status_code == 422