import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.services.authentication.container.container_service import (
    search_containers
)


# =========================================================
# SEARCH CONTAINERS - RETURNS RESULTS
# =========================================================

def test_search_containers_returns_all_available():

    db = MagicMock()

    mock_container = MagicMock()
    mock_container.container_id = 1
    mock_container.provider_id = 1
    mock_container.origin = "Mumbai"
    mock_container.destination = "Dubai"
    mock_container.departure_date = "2025-12-01T10:00:00"
    mock_container.total_capacity_kg = 5000.0
    mock_container.available_capacity_kg = 3000.0
    mock_container.price_per_kg = 2.5
    mock_container.is_available = True

    db.query.return_value.filter.return_value.filter.return_value.all.return_value = [
        mock_container
    ]

    # No filters — broad search returning all available
    db.query.return_value.filter.return_value.all.return_value = [mock_container]

    result = search_containers(
        origin=None,
        destination=None,
        min_capacity_kg=None,
        db=db
    )

    assert isinstance(result, list)


# =========================================================
# SEARCH CONTAINERS - EMPTY RESULTS
# =========================================================

def test_search_containers_no_results():

    db = MagicMock()

    # No containers match
    db.query.return_value.filter.return_value.all.return_value = []

    result = search_containers(
        origin="NonExistentCity",
        destination=None,
        min_capacity_kg=None,
        db=db
    )

    assert result == []


# =========================================================
# SEARCH CONTAINERS - WITH FILTERS
# =========================================================

def test_search_containers_with_origin_filter():

    db = MagicMock()

    # Simulate chained filter calls
    mock_query = db.query.return_value
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = []

    result = search_containers(
        origin="Mumbai",
        destination=None,
        min_capacity_kg=None,
        db=db
    )

    # Query should have been built and called
    db.query.assert_called_once()
    assert isinstance(result, list)


def test_search_containers_with_all_filters():

    db = MagicMock()

    mock_query = db.query.return_value
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = []

    result = search_containers(
        origin="Mumbai",
        destination="Dubai",
        min_capacity_kg=1000.0,
        db=db
    )

    db.query.assert_called_once()
    assert isinstance(result, list)
