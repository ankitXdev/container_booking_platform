from pydantic import BaseModel
from datetime import datetime


class BookingDetailResponse(BaseModel):
    booking_id: int
    container_id: int
    exporter_id: int
    booked_capacity_kg: float
    total_price: float
    status: str
    created_at: datetime
    # Container info
    origin: str
    destination: str
    departure_date: datetime
    price_per_kg: float
    # Exporter info
    exporter_name: str
    exporter_email: str
    # Provider info
    provider_business_name: str
    provider_contact: str
