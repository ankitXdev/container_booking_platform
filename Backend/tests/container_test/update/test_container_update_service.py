import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.services.authentication.container.container_service import (
    update_container
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def create_mock_container(container_id=1, provider_id=1):
    c = MagicMock()
    c.container_id = container_id
    c.provider_id = provider_id
    c.origin = "Mumbai"
    c.destination = "Dubai"
    c.departure_date = "2025-12-01T10:00:00"
    c.total_capacity_kg = 5000.0
    c.available_capacity_kg = 3000.0
    c.price_per_kg = 2.5
    c.is_available = True
    return c


def create_mock_update_data(
    origin="Chennai",
    destination="Singapore",
    departure_date="2025-12-15T08:00:00",
    total_capacity_kg=4000.0,
    available_capacity_kg=2000.0,
    price_per_kg=3.0
):
    data = MagicMock()
    data.origin = origin
    data.destination = destination
    data.departure_date = departure_date
    data.total_capacity_kg = total_capacity_kg
    data.available_capacity_kg = available_capacity_kg
    data.price_per_kg = price_per_kg
    return data


def create_mock_user(user_id=1, role="provider"):
    user = MagicMock()
    user.user_id = user_id
    user.role = role
    return user


def create_mock_provider(provider_id=1, user_id=1):
    provider = MagicMock()
    provider.provider_id = provider_id
    provider.user_id = user_id
    return provider


# =========================================================
# UPDATE CONTAINER - SUCCESS
# =========================================================

def test_update_container_success():

    current_user = create_mock_user(user_id=1)
    db = MagicMock()

    mock_container = create_mock_container(provider_id=1)
    mock_provider = create_mock_provider(provider_id=1, user_id=1)

    # First call: find container, second call: find provider
    db.query.return_value.filter.return_value.first.side_effect = [
        mock_container,
        mock_provider
    ]

    update_data = create_mock_update_data()

    result = update_container(
        container_id=1,
        container_data=update_data,
        current_user=current_user,
        db=db
    )

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(mock_container)

    assert result == {"message": "Container updated successfully"}

    # Fields should be updated on the object
    assert mock_container.origin == "Chennai"
    assert mock_container.destination == "Singapore"
    assert mock_container.price_per_kg == 3.0


# =========================================================
# UPDATE CONTAINER - NOT FOUND
# =========================================================

def test_update_container_not_found():

    current_user = create_mock_user()
    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        update_container(
            container_id=999,
            container_data=create_mock_update_data(),
            current_user=current_user,
            db=db
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Container not found"

    db.commit.assert_not_called()


# =========================================================
# UPDATE CONTAINER - UNAUTHORIZED
# =========================================================

def test_update_container_unauthorized():

    current_user = create_mock_user(user_id=2)
    db = MagicMock()

    # Container belongs to provider_id=1
    mock_container = create_mock_container(provider_id=1)

    # But current user is linked to provider_id=99
    mock_provider = create_mock_provider(provider_id=99, user_id=2)

    db.query.return_value.filter.return_value.first.side_effect = [
        mock_container,
        mock_provider
    ]

    with pytest.raises(HTTPException) as exc_info:
        update_container(
            container_id=1,
            container_data=create_mock_update_data(),
            current_user=current_user,
            db=db
        )

    assert exc_info.value.status_code == 403
    assert "not authorized" in exc_info.value.detail

    db.commit.assert_not_called()


# =========================================================
# UPDATE CONTAINER - INVALID CAPACITY
# =========================================================

def test_update_container_available_exceeds_total():

    current_user = create_mock_user(user_id=1)
    db = MagicMock()

    mock_container = create_mock_container(provider_id=1)
    mock_provider = create_mock_provider(provider_id=1, user_id=1)

    db.query.return_value.filter.return_value.first.side_effect = [
        mock_container,
        mock_provider
    ]

    update_data = create_mock_update_data(
        total_capacity_kg=1000.0,
        available_capacity_kg=9999.0    # invalid
    )

    with pytest.raises(HTTPException) as exc_info:
        update_container(
            container_id=1,
            container_data=update_data,
            current_user=current_user,
            db=db
        )

    assert exc_info.value.status_code == 422
    assert "available_capacity_kg cannot exceed total_capacity_kg" in exc_info.value.detail

    db.commit.assert_not_called()
