import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.services.authentication.container.container_service import (
    update_container_availability
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def create_mock_container(container_id=1, provider_id=1, is_available=True):
    c = MagicMock()
    c.container_id = container_id
    c.provider_id = provider_id
    c.is_available = is_available
    return c


def create_mock_user(user_id=1):
    user = MagicMock()
    user.user_id = user_id
    return user


def create_mock_provider(provider_id=1, user_id=1):
    provider = MagicMock()
    provider.provider_id = provider_id
    provider.user_id = user_id
    return provider


def create_mock_availability_data(is_available=False):
    data = MagicMock()
    data.is_available = is_available
    return data


# =========================================================
# AVAILABILITY UPDATE - MARK UNAVAILABLE
# =========================================================

def test_update_availability_mark_unavailable():

    current_user = create_mock_user(user_id=1)
    db = MagicMock()

    mock_container = create_mock_container(provider_id=1, is_available=True)
    mock_provider = create_mock_provider(provider_id=1, user_id=1)

    db.query.return_value.filter.return_value.first.side_effect = [
        mock_container,
        mock_provider
    ]

    availability_data = create_mock_availability_data(is_available=False)

    result = update_container_availability(
        container_id=1,
        availability_data=availability_data,
        current_user=current_user,
        db=db
    )

    assert mock_container.is_available == False
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(mock_container)

    assert result["message"] == "Container availability updated successfully"
    assert result["is_available"] == False


# =========================================================
# AVAILABILITY UPDATE - MARK AVAILABLE
# =========================================================

def test_update_availability_mark_available():

    current_user = create_mock_user(user_id=1)
    db = MagicMock()

    mock_container = create_mock_container(provider_id=1, is_available=False)
    mock_provider = create_mock_provider(provider_id=1, user_id=1)

    db.query.return_value.filter.return_value.first.side_effect = [
        mock_container,
        mock_provider
    ]

    availability_data = create_mock_availability_data(is_available=True)

    result = update_container_availability(
        container_id=1,
        availability_data=availability_data,
        current_user=current_user,
        db=db
    )

    assert mock_container.is_available == True
    assert result["is_available"] == True


# =========================================================
# AVAILABILITY UPDATE - NOT FOUND
# =========================================================

def test_update_availability_container_not_found():

    current_user = create_mock_user()
    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        update_container_availability(
            container_id=999,
            availability_data=create_mock_availability_data(),
            current_user=current_user,
            db=db
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Container not found"

    db.commit.assert_not_called()


# =========================================================
# AVAILABILITY UPDATE - UNAUTHORIZED
# =========================================================

def test_update_availability_unauthorized():

    current_user = create_mock_user(user_id=2)
    db = MagicMock()

    mock_container = create_mock_container(provider_id=1)
    mock_provider = create_mock_provider(provider_id=99, user_id=2)

    db.query.return_value.filter.return_value.first.side_effect = [
        mock_container,
        mock_provider
    ]

    with pytest.raises(HTTPException) as exc_info:
        update_container_availability(
            container_id=1,
            availability_data=create_mock_availability_data(),
            current_user=current_user,
            db=db
        )

    assert exc_info.value.status_code == 403
    assert "not authorized" in exc_info.value.detail

    db.commit.assert_not_called()
