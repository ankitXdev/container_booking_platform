import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.services.authentication.container.container_service import (
    get_container_details
)


# ---------------------------------------------------------
# Helper
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
    c.provider = MagicMock()
    c.provider.business_name = "ABC Logistics"
    c.provider.contact = "9876543210"
    return c


# =========================================================
# GET DETAILS - SUCCESS
# =========================================================

def test_get_container_details_success():

    db = MagicMock()

    mock_container = create_mock_container()
    db.query.return_value.filter.return_value.first.return_value = mock_container

    result = get_container_details(container_id=1, db=db)

    assert result["container_id"] == 1
    assert result["origin"] == "Mumbai"
    assert result["destination"] == "Dubai"
    assert result["provider_business_name"] == "ABC Logistics"
    assert result["provider_contact"] == "9876543210"


# =========================================================
# GET DETAILS - NOT FOUND
# =========================================================

def test_get_container_details_not_found():

    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_container_details(container_id=999, db=db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Container not found"


# =========================================================
# GET DETAILS - CORRECT FIELDS RETURNED
# =========================================================

def test_get_container_details_returns_provider_info():

    db = MagicMock()

    mock_container = create_mock_container()
    mock_container.provider.business_name = "Global Freight Co."
    mock_container.provider.contact = "+91-9000000001"

    db.query.return_value.filter.return_value.first.return_value = mock_container

    result = get_container_details(container_id=1, db=db)

    assert result["provider_business_name"] == "Global Freight Co."
    assert result["provider_contact"] == "+91-9000000001"
