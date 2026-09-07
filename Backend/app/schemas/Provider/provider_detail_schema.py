from pydantic import BaseModel


class ProviderDetailResponse(BaseModel):
    provider_id: int
    business_name: str
    business_address: str
    contact: str
    email: str
    approval_status: str