from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base
from app.models.user_model import users


class exporter_document(Base):
    __tablename__ = "exporter_documents"

    document_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
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
    user = relationship("users", foreign_keys=[user_id])
    reviewer = relationship("users", foreign_keys=[verified_by])
