from pydantic import BaseModel


class BookingCancelResponse(BaseModel):
    message: str
    booking_id: int
    status: str
