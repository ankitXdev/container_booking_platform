from datetime import datetime
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.exporter_document_model import exporter_document
from app.models.provider_document_model import provider_document
from app.models.provider_details_model import provider_details
from app.utils.file_upload import save_upload_file


# ---------------------------------------------------------------------------
# EXPORTER SERVICES
# ---------------------------------------------------------------------------

def upload_exporter_document(
    document_type: str,
    document_number: str | None,
    file: UploadFile,
    current_user,
    db: Session
):
    if current_user.role != "exporter":
        raise HTTPException(
            status_code=403,
            detail="Only exporters can upload exporter documents"
        )

    url = save_upload_file(file)

    new_doc = exporter_document(
        user_id=current_user.user_id,
        document_type=document_type.upper().strip(),
        document_url=url,
        document_number=document_number.strip() if document_number else None,
        status="PENDING"
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc


def get_exporter_documents(current_user, db: Session):
    if current_user.role != "exporter":
        raise HTTPException(
            status_code=403,
            detail="Only exporters can view their documents"
        )

    return (
        db.query(exporter_document)
        .filter(exporter_document.user_id == current_user.user_id)
        .order_by(exporter_document.uploaded_at.desc())
        .all()
    )


def get_exporter_compliance_status(current_user, db: Session):
    docs = get_exporter_documents(current_user, db)
    if not docs:
        return {
            "is_verified": False,
            "status": "NOT_SUBMITTED",
            "documents": [],
            "message": "Please upload your business registration/IEC documents to unlock booking privileges."
        }

    has_verified = any(d.status == "VERIFIED" for d in docs)
    has_pending = any(d.status == "PENDING" for d in docs)
    has_rejected = any(d.status == "REJECTED" for d in docs)

    if has_verified:
        return {
            "is_verified": True,
            "status": "VERIFIED",
            "documents": docs,
            "message": "Your exporter account is verified and fully active."
        }
    elif has_pending:
        return {
            "is_verified": False,
            "status": "PENDING",
            "documents": docs,
            "message": "Your submitted documents are currently under admin review."
        }
    else:
        return {
            "is_verified": False,
            "status": "REJECTED",
            "documents": docs,
            "message": "Your documents were rejected. Please review rejection notes and re-upload."
        }


# ---------------------------------------------------------------------------
# PROVIDER SERVICES
# ---------------------------------------------------------------------------

def upload_provider_document(
    document_type: str,
    document_number: str | None,
    file: UploadFile,
    current_user,
    db: Session
):
    if current_user.role != "provider":
        raise HTTPException(
            status_code=403,
            detail="Only providers can upload provider documents"
        )

    provider = (
        db.query(provider_details)
        .filter(provider_details.user_id == current_user.user_id)
        .first()
    )

    if not provider:
        raise HTTPException(
            status_code=400,
            detail="Please complete provider profile registration first"
        )

    url = save_upload_file(file)

    new_doc = provider_document(
        provider_id=provider.provider_id,
        document_type=document_type.upper().strip(),
        document_url=url,
        document_number=document_number.strip() if document_number else None,
        status="PENDING"
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc


def get_provider_documents(current_user, db: Session):
    if current_user.role != "provider":
        raise HTTPException(
            status_code=403,
            detail="Only providers can view their documents"
        )

    provider = (
        db.query(provider_details)
        .filter(provider_details.user_id == current_user.user_id)
        .first()
    )

    if not provider:
        return []

    return (
        db.query(provider_document)
        .filter(provider_document.provider_id == provider.provider_id)
        .order_by(provider_document.uploaded_at.desc())
        .all()
    )


def get_provider_compliance_status(current_user, db: Session):
    provider = (
        db.query(provider_details)
        .filter(provider_details.user_id == current_user.user_id)
        .first()
    )

    if not provider:
        return {
            "is_verified": False,
            "status": "NOT_REGISTERED",
            "documents": [],
            "message": "Provider profile registration not completed."
        }

    docs = (
        db.query(provider_document)
        .filter(provider_document.provider_id == provider.provider_id)
        .order_by(provider_document.uploaded_at.desc())
        .all()
    )

    is_approved = provider.approval_status == "approved"
    return {
        "is_verified": is_approved,
        "status": provider.approval_status.upper(),
        "documents": docs,
        "message": f"Provider account status: {provider.approval_status.upper()}"
    }


# ---------------------------------------------------------------------------
# ADMIN REVIEW SERVICES
# ---------------------------------------------------------------------------

def admin_list_pending_documents(current_user, db: Session):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    exporter_docs = (
        db.query(exporter_document)
        .order_by(exporter_document.uploaded_at.desc())
        .all()
    )

    provider_docs = (
        db.query(provider_document)
        .order_by(provider_document.uploaded_at.desc())
        .all()
    )

    formatted_exporter = []
    for d in exporter_docs:
        formatted_exporter.append({
            "document_id": d.document_id,
            "user_id": d.user_id,
            "user_name": d.user.name if d.user else None,
            "user_email": d.user.email if d.user else None,
            "document_type": d.document_type,
            "document_number": d.document_number,
            "document_url": d.document_url,
            "status": d.status,
            "rejection_reason": d.rejection_reason,
            "uploaded_at": d.uploaded_at,
            "verified_at": d.verified_at,
            "verified_by": d.verified_by
        })

    formatted_provider = []
    for d in provider_docs:
        formatted_provider.append({
            "document_id": d.document_id,
            "provider_id": d.provider_id,
            "business_name": d.provider.business_name if d.provider else None,
            "document_type": d.document_type,
            "document_number": d.document_number,
            "document_url": d.document_url,
            "status": d.status,
            "rejection_reason": d.rejection_reason,
            "uploaded_at": d.uploaded_at,
            "verified_at": d.verified_at,
            "verified_by": d.verified_by
        })

    return {
        "exporter_documents": formatted_exporter,
        "provider_documents": formatted_provider
    }


def admin_review_exporter_document(
    document_id: int,
    status: str,
    rejection_reason: str | None,
    current_user,
    db: Session
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    status_upper = status.upper().strip()
    if status_upper not in ["VERIFIED", "REJECTED"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be either VERIFIED or REJECTED"
        )

    doc = (
        db.query(exporter_document)
        .filter(exporter_document.document_id == document_id)
        .first()
    )

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    doc.status = status_upper
    doc.verified_by = current_user.user_id
    doc.verified_at = datetime.utcnow()
    doc.rejection_reason = rejection_reason if status_upper == "REJECTED" else None

    db.commit()
    db.refresh(doc)
    return doc


def admin_review_provider_document(
    document_id: int,
    status: str,
    rejection_reason: str | None,
    current_user,
    db: Session
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    status_upper = status.upper().strip()
    if status_upper not in ["VERIFIED", "REJECTED"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be either VERIFIED or REJECTED"
        )

    doc = (
        db.query(provider_document)
        .filter(provider_document.document_id == document_id)
        .first()
    )

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    doc.status = status_upper
    doc.verified_by = current_user.user_id
    doc.verified_at = datetime.utcnow()
    doc.rejection_reason = rejection_reason if status_upper == "REJECTED" else None

    db.commit()
    db.refresh(doc)
    return doc
