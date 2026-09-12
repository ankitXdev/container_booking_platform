from pydantic import BaseModel


class BookingStatusUpdate(BaseModel):
    status: str
    # Allowed values: "confirmed" | "cancelled"


class BookingStatusResponse(BaseModel):
    message: str
    status: str
