from pydantic import BaseModel, Field
from datetime import datetime


class ContainerCreate(BaseModel):
    origin: str = Field(min_length=2, max_length=255)
    destination: str = Field(min_length=2, max_length=255)
    departure_date: datetime
    total_capacity_kg: float = Field(gt=0)
    available_capacity_kg: float = Field(gt=0)
    price_per_kg: float = Field(gt=0)


class ContainerCreateResponse(BaseModel):
    message: str
    container_id: int
