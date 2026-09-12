from pydantic import BaseModel


class PendingProviderItem(BaseModel):
    provider_id: int
    user_id: int
    business_name: str
    business_address: str
    contact: str
    approval_status: str
    email: str
