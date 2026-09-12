from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.config.database import get_db
from app.security.dependencies import get_current_user
from app.schemas.Document.document_schema import (
    DocumentResponse,
    DocumentReviewRequest,
    ComplianceStatusResponse,
)
from app.services.authentication.document.document_service import (
    upload_exporter_document,
    get_exporter_documents,
    get_exporter_compliance_status,
    upload_provider_document,
    get_provider_documents,
    get_provider_compliance_status,
    admin_list_pending_documents,
    admin_review_exporter_document,
    admin_review_provider_document,
)

router = APIRouter(
    tags=["Documents & Compliance"]
)

# ---------------------------------------------------------------------------
# EXPORTER ROUTES
# ---------------------------------------------------------------------------

@router.post("/documents/exporter/upload", response_model=DocumentResponse)
def api_upload_exporter_document(
    document_type: str = Form(...),
    document_number: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return upload_exporter_document(
        document_type=document_type,
        document_number=document_number,
        file=file,
        current_user=current_user,
        db=db
    )


@router.get("/documents/exporter/me", response_model=List[DocumentResponse])
def api_get_exporter_documents(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_exporter_documents(current_user=current_user, db=db)


@router.get("/documents/exporter/status", response_model=ComplianceStatusResponse)
def api_get_exporter_compliance_status(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_exporter_compliance_status(current_user=current_user, db=db)


# ---------------------------------------------------------------------------
# PROVIDER ROUTES
# ---------------------------------------------------------------------------

@router.post("/documents/provider/upload", response_model=DocumentResponse)
def api_upload_provider_document(
    document_type: str = Form(...),
    document_number: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return upload_provider_document(
        document_type=document_type,
        document_number=document_number,
        file=file,
        current_user=current_user,
        db=db
    )


@router.get("/documents/provider/me", response_model=List[DocumentResponse])
def api_get_provider_documents(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_provider_documents(current_user=current_user, db=db)


@router.get("/documents/provider/status", response_model=ComplianceStatusResponse)
def api_get_provider_compliance_status(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_provider_compliance_status(current_user=current_user, db=db)


# ---------------------------------------------------------------------------
# ADMIN REVIEW ROUTES
# ---------------------------------------------------------------------------

@router.get("/admin/documents")
def api_admin_list_documents(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return admin_list_pending_documents(current_user=current_user, db=db)


@router.patch("/admin/documents/exporter/{document_id}/review", response_model=DocumentResponse)
def api_admin_review_exporter_document(
    document_id: int,
    review_data: DocumentReviewRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return admin_review_exporter_document(
        document_id=document_id,
        status=review_data.status,
        rejection_reason=review_data.rejection_reason,
        current_user=current_user,
        db=db
    )


@router.patch("/admin/documents/provider/{document_id}/review", response_model=DocumentResponse)
def api_admin_review_provider_document(
    document_id: int,
    review_data: DocumentReviewRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return admin_review_provider_document(
        document_id=document_id,
        status=review_data.status,
        rejection_reason=review_data.rejection_reason,
        current_user=current_user,
        db=db
    )
