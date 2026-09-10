import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.services.authentication.container.container_service import (
    delete_container
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def create_mock_container(container_id=1, provider_id=1):
    c = MagicMock()
    c.container_id = container_id
    c.provider_id = provider_id
    return c


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
# DELETE CONTAINER - SUCCESS
# =========================================================

def test_delete_container_success():

    current_user = create_mock_user(user_id=1)
    db = MagicMock()

    mock_container = create_mock_container(provider_id=1)
    mock_provider = create_mock_provider(provider_id=1, user_id=1)

    db.query.return_value.filter.return_value.first.side_effect = [
        mock_container,
        mock_provider
    ]

    result = delete_container(
        container_id=1,
        current_user=current_user,
        db=db
    )

    db.delete.assert_called_once_with(mock_container)
    db.commit.assert_called_once()

    assert result == {"message": "Container deleted successfully"}


# =========================================================
# DELETE CONTAINER - NOT FOUND
# =========================================================

def test_delete_container_not_found():

    current_user = create_mock_user()
    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        delete_container(container_id=999, current_user=current_user, db=db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Container not found"

    db.delete.assert_not_called()
    db.commit.assert_not_called()


# =========================================================
# DELETE CONTAINER - UNAUTHORIZED
# =========================================================

def test_delete_container_unauthorized():

    current_user = create_mock_user(user_id=2)
    db = MagicMock()

    # Container belongs to provider_id=1
    mock_container = create_mock_container(provider_id=1)

    # Current user has provider_id=99
    mock_provider = create_mock_provider(provider_id=99, user_id=2)

    db.query.return_value.filter.return_value.first.side_effect = [
        mock_container,
        mock_provider
    ]

    with pytest.raises(HTTPException) as exc_info:
        delete_container(container_id=1, current_user=current_user, db=db)

    assert exc_info.value.status_code == 403
    assert "not authorized" in exc_info.value.detail

    db.delete.assert_not_called()
    db.commit.assert_not_called()
