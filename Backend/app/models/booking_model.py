from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base
from app.models.user_model import users
from app.models.container_model import container


class booking(Base):

    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True)

    container_id = Column(
        Integer,
        ForeignKey("containers.container_id"),
        nullable=False
    )

    exporter_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    booked_capacity_kg = Column(Float, nullable=False)

    total_price = Column(Float, nullable=False)

    status = Column(
        String,
        nullable=False,
        default="pending"
        # values: pending | confirmed | cancelled
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

    # Relationships
    container = relationship(container)
    exporter = relationship(users, foreign_keys=[exporter_id])
