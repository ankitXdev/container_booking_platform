from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base
from app.models.provider_details_model import provider_details
from app.models.user_model import users


class provider_document(Base):
    __tablename__ = "provider_documents"

    document_id = Column(Integer, primary_key=True, autoincrement=True)

    provider_id = Column(
        Integer,
        ForeignKey("provider_details.provider_id", ondelete="CASCADE"),
        nullable=False
    )

    document_type = Column(String(100), nullable=False)

    document_url = Column(Text, nullable=False)

    document_number = Column(String(100), nullable=True)

    status = Column(
        String(20),
        nullable=False,
        default="PENDING"
    )

    rejection_reason = Column(Text, nullable=True)

    uploaded_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    verified_at = Column(
        DateTime,
        nullable=True
    )

    verified_by = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True
    )

    # Relationships
    provider = relationship("provider_details", foreign_keys=[provider_id])
    reviewer = relationship("users", foreign_keys=[verified_by])
