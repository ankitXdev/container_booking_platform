import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app


client = TestClient(app)


# =========================================================
# SEARCH CONTAINERS - SUCCESS (no filters)
# =========================================================

def test_search_containers_route_success():

    expected_response = [
        {
            "container_id": 1,
            "provider_id": 1,
            "origin": "Mumbai",
            "destination": "Dubai",
            "departure_date": "2025-12-01T10:00:00",
            "total_capacity_kg": 5000.0,
            "available_capacity_kg": 3000.0,
            "price_per_kg": 2.5,
            "is_available": True
        }
    ]

    with patch(
        "app.routes.Container.container_router.search_containers_controller",
        return_value=expected_response
    ):
        response = client.get("/containers/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert data[0]["container_id"] == 1
    assert data[0]["origin"] == "Mumbai"


# =========================================================
# SEARCH CONTAINERS - WITH QUERY PARAMS
# =========================================================

def test_search_containers_route_with_filters():

    with patch(
        "app.routes.Container.container_router.search_containers_controller",
        return_value=[]
    ):
        response = client.get(
            "/containers/",
            params={
                "origin": "Mumbai",
                "destination": "Dubai",
                "min_capacity_kg": 1000.0
            }
        )

    assert response.status_code == 200
    assert response.json() == []


# =========================================================
# SEARCH CONTAINERS - EMPTY RESULT
# =========================================================

def test_search_containers_route_empty_result():

    with patch(
        "app.routes.Container.container_router.search_containers_controller",
        return_value=[]
    ):
        response = client.get("/containers/")

    assert response.status_code == 200
    assert response.json() == []


# =========================================================
# SEARCH CONTAINERS - PUBLIC (no auth required)
# =========================================================

def test_search_containers_route_no_auth_required():

    # GET /containers/ is public — no token needed
    app.dependency_overrides.clear()

    with patch(
        "app.routes.Container.container_router.search_containers_controller",
        return_value=[]
    ):
        response = client.get("/containers/")

    # Should not be 401 or 403
    assert response.status_code == 200
