from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    container_id: int
    booked_capacity_kg: float = Field(gt=0)


class BookingCreateResponse(BaseModel):
    message: str
    booking_id: int
    total_price: float
    status: str
