from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base
from app.models.booking_model import booking


class payment(Base):

    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.booking_id"),
        nullable=False,
        unique=True          # one payment record per booking
    )

    razorpay_order_id = Column(String, nullable=False, unique=True)

    # Filled after POST /payments/verify
    razorpay_payment_id = Column(String, nullable=True)

    razorpay_signature = Column(String, nullable=True)

    amount = Column(Float, nullable=False)          # in INR (rupees)

    currency = Column(String(10), nullable=False, default="INR")

    status = Column(
        String,
        nullable=False,
        default="created"
        # values: created | paid | failed
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

    # Relationship
    booking_ref = relationship(booking)
