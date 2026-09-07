from sqlalchemy import String, Integer, Column, ForeignKey, DateTime
from app.config.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.user_model import users


class provider_details(Base):

    __tablename__ = "provider_details"

    provider_id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("user.user_id"),
        nullable=False,
        unique=True
    )

    business_name = Column(String, nullable=False)

    business_address = Column(String, nullable=False)

    contact = Column(String, nullable=False)

    approval_status = Column(
        String,
        nullable=False,
        default="pending"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship(users)