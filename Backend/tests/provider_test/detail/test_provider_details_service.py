from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException

from app.services.authentication.provider.provider_service import (
    get_provider_details
)


class MockUser:
    user_id = 1
    role = "exporter"


def test_get_approved_provider_details():
    db = MagicMock()
    mock_provider = SimpleNamespace(
        provider_id=15,
        business_name="ABC Logistics",
        business_address="Mumbai, Maharashtra",
        contact="9876543210",
        approval_status="approved",
        user=SimpleNamespace(
            email="abc@example.com"
        )
    )
    db.query.return_value.filter.return_value.first.return_value = mock_provider

    result = get_provider_details(
        provider_id=15,
        current_user=MockUser(),
        db=db
    )

    assert result["provider_id"] == 15
    assert result["business_name"] == "ABC Logistics"
    assert result["business_address"] == "Mumbai, Maharashtra"
    assert result["contact"] == "9876543210"
    assert result["email"] == "abc@example.com"
    assert result["approval_status"] == "approved"


def test_get_non_existing_provider():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:

        get_provider_details(
            provider_id=99999,
            current_user=MockUser(),
            db=db
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Provider not found"


def test_get_pending_provider():
    db = MagicMock()
    mock_provider = SimpleNamespace(
        provider_id=16,
        approval_status="pending"
    )
    db.query.return_value.filter.return_value.first.return_value = mock_provider

    with pytest.raises(HTTPException) as exc_info:

        get_provider_details(
            provider_id=16,
            current_user=MockUser(),
            db=db
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Provider not found"


def test_get_rejected_provider():
    db = MagicMock()
    mock_provider = SimpleNamespace(
        provider_id=17,
        approval_status="rejected"
    )
    db.query.return_value.filter.return_value.first.return_value = mock_provider

    with pytest.raises(HTTPException) as exc_info:

        get_provider_details(
            provider_id=17,
            current_user=MockUser(),
            db=db
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Provider not found"