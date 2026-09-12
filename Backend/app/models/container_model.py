from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base
from app.models.provider_details_model import provider_details


class container(Base):

    __tablename__ = "containers"

    container_id = Column(Integer, primary_key=True)

    provider_id = Column(
        Integer,
        ForeignKey("provider_details.provider_id"),
        nullable=False
    )

    origin = Column(String(255), nullable=False)

    destination = Column(String(255), nullable=False)

    departure_date = Column(DateTime, nullable=False)

    total_capacity_kg = Column(Float, nullable=False)

    available_capacity_kg = Column(Float, nullable=False)

    price_per_kg = Column(Float, nullable=False)

    is_available = Column(
        Boolean,
        nullable=False,
        default=True
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

    provider = relationship(provider_details)
