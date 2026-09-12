import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from io import BytesIO

from app.main import app
from app.security.dependencies import get_current_user

client = TestClient(app)


def create_mock_user(user_id=1, role="exporter", name="Test Exporter", email="exporter@test.com"):
    class MockUser:
        pass
    u = MockUser()
    u.user_id = user_id
    u.role = role
    u.name = name
    u.email = email
    return u


# =========================================================
# EXPORTER DOCUMENT UPLOAD & STATUS TESTS
# =========================================================

def test_exporter_upload_document_success():
    mock_user = create_mock_user(role="exporter")
    app.dependency_overrides[get_current_user] = lambda: mock_user

    mock_doc = MagicMock()
    mock_doc.document_id = 101
    mock_doc.document_type = "IEC"
    mock_doc.document_url = "/uploads/documents/fake_iec.pdf"
    mock_doc.document_number = "IEC123456"
    mock_doc.status = "PENDING"
    mock_doc.rejection_reason = None
    mock_doc.uploaded_at = "2026-09-12T00:00:00"
    mock_doc.verified_at = None
    mock_doc.verified_by = None

    with patch(
        "app.routes.Document.document_router.upload_exporter_document",
        return_value=mock_doc
    ):
        file_content = b"%PDF-1.4 test dummy pdf content"
        response = client.post(
            "/documents/exporter/upload",
            data={"document_type": "IEC", "document_number": "IEC123456"},
            files={"file": ("iec.pdf", BytesIO(file_content), "application/pdf")}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["document_id"] == 101
    assert data["status"] == "PENDING"


def test_exporter_get_compliance_status_success():
    mock_user = create_mock_user(role="exporter")
    app.dependency_overrides[get_current_user] = lambda: mock_user

    expected = {
        "is_verified": True,
        "status": "VERIFIED",
        "documents": [],
        "message": "Your exporter account is verified and fully active."
    }

    with patch(
        "app.routes.Document.document_router.get_exporter_compliance_status",
        return_value=expected
    ):
        response = client.get("/documents/exporter/status")

    assert response.status_code == 200
    data = response.json()
    assert data["is_verified"] is True
    assert data["status"] == "VERIFIED"


# =========================================================
# ADMIN REVIEW TESTS
# =========================================================

def test_admin_review_exporter_document_success():
    admin_user = create_mock_user(user_id=99, role="admin")
    app.dependency_overrides[get_current_user] = lambda: admin_user

    mock_doc = MagicMock()
    mock_doc.document_id = 101
    mock_doc.document_type = "IEC"
    mock_doc.document_url = "/uploads/documents/fake_iec.pdf"
    mock_doc.document_number = "IEC123456"
    mock_doc.status = "VERIFIED"
    mock_doc.rejection_reason = None
    mock_doc.uploaded_at = "2026-09-12T00:00:00"
    mock_doc.verified_at = "2026-09-12T00:05:00"
    mock_doc.verified_by = 99

    with patch(
        "app.routes.Document.document_router.admin_review_exporter_document",
        return_value=mock_doc
    ):
        response = client.patch(
            "/admin/documents/exporter/101/review",
            json={"status": "VERIFIED"}
        )

    assert response.status_code == 200
    assert response.json()["status"] == "VERIFIED"
