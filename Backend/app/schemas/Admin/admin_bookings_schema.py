from pydantic import BaseModel
from datetime import datetime


class AdminBookingItem(BaseModel):
    booking_id: int
    container_id: int
    exporter_id: int
    exporter_name: str
    exporter_email: str
    provider_business_name: str
    origin: str
    destination: str
    booked_capacity_kg: float
    total_price: float
    status: str
    created_at: datetime
