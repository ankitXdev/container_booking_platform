from pydantic import BaseModel
from datetime import datetime


class BookingListItem(BaseModel):
    booking_id: int
    container_id: int
    exporter_id: int
    booked_capacity_kg: float
    total_price: float
    status: str
    origin: str
    destination: str
    departure_date: datetime
    created_at: datetime
