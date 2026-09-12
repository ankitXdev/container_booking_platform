import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.services.authentication.admin.admin_service import (
    get_pending_providers,
    approve_provider,
    reject_provider,
    get_platform_stats,
    get_all_bookings
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def create_mock_user(role="admin"):
    user = MagicMock()
    user.role = role
    return user


def create_mock_provider(
    provider_id=1,
    user_id=1,
    approval_status="pending"
):
    p = MagicMock()
    p.provider_id = provider_id
    p.user_id = user_id
    p.business_name = "ABC Logistics"
    p.business_address = "Mumbai, India"
    p.contact = "9876543210"
    p.approval_status = approval_status
    p.user = MagicMock()
    p.user.email = "abc@example.com"
    return p


# =========================================================
# GET PENDING PROVIDERS - SUCCESS
# =========================================================

def test_get_pending_providers_success():

    current_user = create_mock_user(role="admin")
    db = MagicMock()

    mock_provider = create_mock_provider(approval_status="pending")

    db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
        mock_provider
    ]

    result = get_pending_providers(current_user, db)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["approval_status"] == "pending"


# =========================================================
# GET PENDING PROVIDERS - NON-ADMIN BLOCKED
# =========================================================

def test_get_pending_providers_non_admin_blocked():

    current_user = create_mock_user(role="exporter")
    db = MagicMock()

    with pytest.raises(HTTPException) as exc_info:
        get_pending_providers(current_user, db)

    assert exc_info.value.status_code == 403
    assert "Admin access required" in exc_info.value.detail

    db.query.assert_not_called()


# =========================================================
# APPROVE PROVIDER - SUCCESS
# =========================================================

def test_approve_provider_success():

    current_user = create_mock_user(role="admin")
    db = MagicMock()

    mock_provider = create_mock_provider(approval_status="pending")
    db.query.return_value.filter.return_value.first.return_value = mock_provider

    result = approve_provider(provider_id=1, current_user=current_user, db=db)

    assert mock_provider.approval_status == "approved"
    db.commit.assert_called_once()
    assert result["message"] == "Provider approved successfully"
    assert result["approval_status"] == "approved"


# =========================================================
# APPROVE PROVIDER - NOT FOUND
# =========================================================

def test_approve_provider_not_found():

    current_user = create_mock_user(role="admin")
    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        approve_provider(provider_id=999, current_user=current_user, db=db)

    assert exc_info.value.status_code == 404
    assert "Provider not found" in exc_info.value.detail


# =========================================================
# APPROVE PROVIDER - IDEMPOTENT (already approved)
# =========================================================

def test_approve_provider_already_approved_is_idempotent():

    current_user = create_mock_user(role="admin")
    db = MagicMock()

    mock_provider = create_mock_provider(approval_status="approved")
    db.query.return_value.filter.return_value.first.return_value = mock_provider

    result = approve_provider(provider_id=1, current_user=current_user, db=db)

    assert result["message"] == "Provider is already approved"

    # No database write needed for already-approved
    db.commit.assert_not_called()


# =========================================================
# REJECT PROVIDER - SUCCESS
# =========================================================

def test_reject_provider_success():

    current_user = create_mock_user(role="admin")
    db = MagicMock()

    mock_provider = create_mock_provider(approval_status="pending")
    db.query.return_value.filter.return_value.first.return_value = mock_provider

    result = reject_provider(provider_id=1, current_user=current_user, db=db)

    assert mock_provider.approval_status == "rejected"
    db.commit.assert_called_once()
    assert result["approval_status"] == "rejected"


# =========================================================
# REJECT PROVIDER - NON-ADMIN BLOCKED
# =========================================================

def test_reject_provider_non_admin_blocked():

    current_user = create_mock_user(role="provider")
    db = MagicMock()

    with pytest.raises(HTTPException) as exc_info:
        reject_provider(provider_id=1, current_user=current_user, db=db)

    assert exc_info.value.status_code == 403

    db.query.assert_not_called()


# =========================================================
# GET PLATFORM STATS - SUCCESS
# =========================================================

def test_get_platform_stats_success():

    current_user = create_mock_user(role="admin")
    db = MagicMock()

    # All scalar() calls return simple integers
    db.query.return_value.scalar.return_value = 0
    db.query.return_value.filter.return_value.scalar.return_value = 0

    result = get_platform_stats(current_user, db)

    assert "total_users" in result
    assert "providers" in result
    assert "containers" in result
    assert "bookings" in result
    assert "total_revenue" in result


# =========================================================
# GET PLATFORM STATS - NON-ADMIN BLOCKED
# =========================================================

def test_get_platform_stats_non_admin_blocked():

    current_user = create_mock_user(role="exporter")
    db = MagicMock()

    with pytest.raises(HTTPException) as exc_info:
        get_platform_stats(current_user, db)

    assert exc_info.value.status_code == 403


# =========================================================
# GET ALL BOOKINGS - SUCCESS
# =========================================================

def test_get_all_bookings_success():

    current_user = create_mock_user(role="admin")
    db = MagicMock()

    db.query.return_value.order_by.return_value.all.return_value = []

    result = get_all_bookings(current_user, db)

    assert isinstance(result, list)


# =========================================================
# GET ALL BOOKINGS - NON-ADMIN BLOCKED
# =========================================================

def test_get_all_bookings_non_admin_blocked():

    current_user = create_mock_user(role="exporter")
    db = MagicMock()

    with pytest.raises(HTTPException) as exc_info:
        get_all_bookings(current_user, db)

    assert exc_info.value.status_code == 403

    db.query.assert_not_called()
