from types import SimpleNamespace
from unittest.mock import MagicMock

from app.services.authentication.provider.provider_service import search_provider


def test_search_provider_returns_multiple_approved_providers():
    # Arrange
    db = MagicMock()

    provider_1 = SimpleNamespace(
        provider_id=1,
        business_name="Sharma Agro Services",
        business_address="Lucknow",
        contact="9876543210",
        approval_status="approved",
        user=SimpleNamespace(
            email="sharma1@example.com"
        )
    )

    provider_2 = SimpleNamespace(
        provider_id=2,
        business_name="Sharma Agro Services",
        business_address="Kanpur",
        contact="9123456780",
        approval_status="approved",
        user=SimpleNamespace(
            email="sharma2@example.com"
        )
    )

    db.query.return_value.filter.return_value.all.return_value = [
        provider_1,
        provider_2
    ]

    # Act
    result = search_provider("Sharma", db)

    # Assert
    assert len(result) == 2

    assert result[0] == {
        "provider_id": 1,
        "business_name": "Sharma Agro Services",
        "business_address": "Lucknow",
        "contact": "9876543210",
        "email": "sharma1@example.com"
    }

    assert result[1] == {
        "provider_id": 2,
        "business_name": "Sharma Agro Services",
        "business_address": "Kanpur",
        "contact": "9123456780",
        "email": "sharma2@example.com"
    }


def test_search_provider_returns_empty_list_when_no_provider_found():
    # Arrange
    db = MagicMock()

    db.query.return_value.filter.return_value.all.return_value = []

    # Act
    result = search_provider("NonExistingBusiness", db)

    # Assert
    assert result == []


def test_search_provider_strips_search_term():
    # Arrange
    db = MagicMock()

    db.query.return_value.filter.return_value.all.return_value = []

    # Act
    search_provider("   Sharma   ", db)

    # Assert
    db.query.assert_called_once()


def test_search_provider_returns_only_approved_providers():
    # Arrange
    db = MagicMock()

    provider = SimpleNamespace(
        provider_id=1,
        business_name="Sharma Agro",
        business_address="Lucknow",
        contact="9876543210",
        approval_status="approved",
        user=SimpleNamespace(
            email="sharma@example.com"
        )
    )

    db.query.return_value.filter.return_value.all.return_value = [provider]

    # Act
    result = search_provider("Sharma", db)

    # Assert
    assert len(result) == 1
    assert result[0]["provider_id"] == 1
    assert result[0]["business_name"] == "Sharma Agro"