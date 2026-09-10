import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from app.services.authentication.container.container_service import (
    create_container
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def create_mock_container_data(
    origin="Mumbai",
    destination="Dubai",
    departure_date="2025-12-01T10:00:00",
    total_capacity_kg=5000.0,
    available_capacity_kg=3000.0,
    price_per_kg=2.5
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


def create_mock_provider(provider_id=1, user_id=1, approval_status="approved"):
    provider = MagicMock()
    provider.provider_id = provider_id
    provider.user_id = user_id
    provider.approval_status = approval_status
    return provider


# =========================================================
# CREATE CONTAINER - SUCCESS
# =========================================================

def test_create_container_success():

    container_data = create_mock_container_data()
    current_user = create_mock_user()
    db = MagicMock()

    mock_provider = create_mock_provider()

    # First query returns provider profile
    db.query.return_value.filter.return_value.first.return_value = mock_provider

    with patch(
        "app.services.authentication.container.container_service.container"
    ) as mock_container_model:

        new_container = MagicMock()
        new_container.container_id = 1
        mock_container_model.return_value = new_container

        result = create_container(container_data, current_user, db)

    db.add.assert_called_once_with(new_container)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_container)

    assert result["message"] == "Container listing created successfully"
    assert result["container_id"] == 1


# =========================================================
# CREATE CONTAINER - WRONG ROLE
# =========================================================

def test_create_container_wrong_role():

    container_data = create_mock_container_data()
    current_user = create_mock_user(role="exporter")
    db = MagicMock()

    with pytest.raises(HTTPException) as exc_info:
        create_container(container_data, current_user, db)

    assert exc_info.value.status_code == 403
    assert "Only providers" in exc_info.value.detail

    # Database must not be touched
    db.add.assert_not_called()
    db.commit.assert_not_called()


# =========================================================
# CREATE CONTAINER - PROVIDER NOT FOUND
# =========================================================

def test_create_container_no_provider_profile():

    container_data = create_mock_container_data()
    current_user = create_mock_user(role="provider")
    db = MagicMock()

    # No provider profile exists
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        create_container(container_data, current_user, db)

    assert exc_info.value.status_code == 403
    assert "Provider profile not found" in exc_info.value.detail

    db.add.assert_not_called()
    db.commit.assert_not_called()


# =========================================================
# CREATE CONTAINER - PROVIDER NOT APPROVED
# =========================================================

def test_create_container_provider_not_approved():

    container_data = create_mock_container_data()
    current_user = create_mock_user(role="provider")
    db = MagicMock()

    mock_provider = create_mock_provider(approval_status="pending")
    db.query.return_value.filter.return_value.first.return_value = mock_provider

    with pytest.raises(HTTPException) as exc_info:
        create_container(container_data, current_user, db)

    assert exc_info.value.status_code == 403
    assert "pending admin approval" in exc_info.value.detail

    db.add.assert_not_called()
    db.commit.assert_not_called()


# =========================================================
# CREATE CONTAINER - INVALID CAPACITY
# =========================================================

def test_create_container_available_exceeds_total():

    container_data = create_mock_container_data(
        total_capacity_kg=1000.0,
        available_capacity_kg=2000.0   # invalid: available > total
    )
    current_user = create_mock_user(role="provider")
    db = MagicMock()

    mock_provider = create_mock_provider()
    db.query.return_value.filter.return_value.first.return_value = mock_provider

    with pytest.raises(HTTPException) as exc_info:
        create_container(container_data, current_user, db)

    assert exc_info.value.status_code == 422
    assert "available_capacity_kg cannot exceed total_capacity_kg" in exc_info.value.detail

    db.add.assert_not_called()
    db.commit.assert_not_called()
