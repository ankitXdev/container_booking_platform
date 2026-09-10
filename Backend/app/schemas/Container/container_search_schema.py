from pydantic import BaseModel
from datetime import datetime


class ContainerSearchResponse(BaseModel):
    container_id: int
    provider_id: int
    origin: str
    destination: str
    departure_date: datetime
    total_capacity_kg: float
    available_capacity_kg: float
    price_per_kg: float
    is_available: bool
