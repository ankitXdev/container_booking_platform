from pydantic import BaseModel


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class VerifyPaymentResponse(BaseModel):
    message: str
    booking_id: int
    payment_id: int
    status: str
