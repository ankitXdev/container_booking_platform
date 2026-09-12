from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_id: int
    document_type: str
    document_url: str
    document_number: Optional[str] = None
    status: str
    rejection_reason: Optional[str] = None
    uploaded_at: datetime
    verified_at: Optional[datetime] = None
    verified_by: Optional[int] = None


class DocumentReviewRequest(BaseModel):
    status: str  # 'VERIFIED' or 'REJECTED'
    rejection_reason: Optional[str] = None


class ComplianceStatusResponse(BaseModel):
    is_verified: bool
    status: str  # 'NOT_SUBMITTED', 'PENDING', 'VERIFIED', 'REJECTED'
    documents: List[DocumentResponse]
    message: str
