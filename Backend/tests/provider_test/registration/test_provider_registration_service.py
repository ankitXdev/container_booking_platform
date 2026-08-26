import pytest

from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from app.services.authentication.provider.provider_service import (
    register_provider
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def create_mock_provider(
    business_name="ABC Logistics",
    business_address="Mumbai, Maharashtra",
    contact="9876543210"
):
    provider = MagicMock()

    provider.business_name = business_name
    provider.business_address = business_address
    provider.contact = contact

    return provider


def create_mock_user(
    user_id=1,
    role="provider"
):
    user = MagicMock()

    user.user_id = user_id
    user.role = role

    return user


# =========================================================
# REGISTER PROVIDER TESTS
# =========================================================

def test_register_provider_success():

    provider = create_mock_provider()
    current_user = create_mock_user()
    db = MagicMock()

    # No existing provider profile
    db.query.return_value.filter.return_value.first.return_value = None

    # Mock provider_details so SQLAlchemy mapper is not triggered
    with patch(
        "app.services.authentication.provider.provider_service.provider_details"
    ) as mock_provider_details:

        # Mock newly created provider
        new_provider = MagicMock()
        new_provider.provider_id = 1
        new_provider.approval_status = "pending"

        mock_provider_details.return_value = new_provider

        result = register_provider(
            provider,
            current_user,
            db
        )

    # provider_details should be created
    mock_provider_details.assert_called_once_with(
        user_id=current_user.user_id,
        business_name=provider.business_name,
        contact=provider.contact,
        business_address=provider.business_address,
        approval_status="pending"
    )

    # Database operations
    db.add.assert_called_once_with(new_provider)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_provider)

    # Response
    assert result == {
        "message": "Provider registration successful",
        "provider_id": 1,
        "approval_status": "pending"
    }


def test_register_provider_invalid_role():

    provider = create_mock_provider()

    current_user = create_mock_user(
        role="exporter"
    )

    db = MagicMock()

    with pytest.raises(
        HTTPException,
        match="Only users with provider role can register as a provider"
    ):
        register_provider(
            provider,
            current_user,
            db
        )

    # Database should never be touched
    db.query.assert_not_called()
    db.add.assert_not_called()
    db.commit.assert_not_called()
    db.refresh.assert_not_called()


def test_register_provider_already_exists():

    provider = create_mock_provider()
    current_user = create_mock_user()

    db = MagicMock()

    # Existing provider
    existing_provider = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = (
        existing_provider
    )

    with pytest.raises(
        HTTPException,
        match="Provider profile already exists"
    ):
        register_provider(
            provider,
            current_user,
            db
        )

    # New provider should not be created
    db.add.assert_not_called()

    # Transaction should not happen
    db.commit.assert_not_called()
    db.refresh.assert_not_called()


def test_register_provider_uses_current_user_id():

    provider = create_mock_provider()

    current_user = create_mock_user(
        user_id=25
    )

    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    with patch(
        "app.services.authentication.provider.provider_service.provider_details"
    ) as mock_provider_details:

        new_provider = MagicMock()
        new_provider.provider_id = 1
        new_provider.approval_status = "pending"

        mock_provider_details.return_value = new_provider

        register_provider(
            provider,
            current_user,
            db
        )

    # Check user_id passed to model
    mock_provider_details.assert_called_once()

    call_kwargs = mock_provider_details.call_args.kwargs

    assert call_kwargs["user_id"] == 25


def test_register_provider_saves_correct_data():

    provider = create_mock_provider(
        business_name="Global Shipping",
        business_address="Delhi, India",
        contact="9999999999"
    )

    current_user = create_mock_user(
        user_id=10
    )

    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    with patch(
        "app.services.authentication.provider.provider_service.provider_details"
    ) as mock_provider_details:

        new_provider = MagicMock()
        new_provider.provider_id = 1
        new_provider.approval_status = "pending"

        mock_provider_details.return_value = new_provider

        register_provider(
            provider,
            current_user,
            db
        )

    call_kwargs = mock_provider_details.call_args.kwargs

    assert call_kwargs["user_id"] == 10
    assert call_kwargs["business_name"] == "Global Shipping"
    assert call_kwargs["business_address"] == "Delhi, India"
    assert call_kwargs["contact"] == "9999999999"
    assert call_kwargs["approval_status"] == "pending"


def test_register_provider_commits_transaction():

    provider = create_mock_provider()
    current_user = create_mock_user()

    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    with patch(
        "app.services.authentication.provider.provider_service.provider_details"
    ) as mock_provider_details:

        new_provider = MagicMock()
        new_provider.provider_id = 1
        new_provider.approval_status = "pending"

        mock_provider_details.return_value = new_provider

        register_provider(
            provider,
            current_user,
            db
        )

    db.add.assert_called_once_with(new_provider)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_provider)