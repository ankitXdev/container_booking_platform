from pydantic import BaseModel


class CreateOrderRequest(BaseModel):
    booking_id: int


class CreateOrderResponse(BaseModel):
    razorpay_order_id: str
    amount: float           # rupees
    amount_in_paise: int    # for Razorpay JS checkout
    currency: str
    booking_id: int
    key_id: str             # public key — safe to expose to frontend
