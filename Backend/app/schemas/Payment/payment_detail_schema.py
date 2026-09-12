from pydantic import BaseModel
from datetime import datetime


class PaymentDetailResponse(BaseModel):
    payment_id: int
    booking_id: int
    razorpay_order_id: str
    razorpay_payment_id: str | None
    amount: float
    currency: str
    status: str
    created_at: datetime
    # Booking summary
    origin: str
    destination: str
    booked_capacity_kg: float
    total_price: float
    booking_status: str
