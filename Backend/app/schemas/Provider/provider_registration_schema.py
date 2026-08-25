from pydantic import BaseModel, Field


class ProviderCreate(BaseModel):
    business_name: str = Field(min_length=2, max_length=100)
    business_address: str = Field(min_length=5, max_length=255)
    contact: str = Field(min_length=10, max_length=15)


class ProviderResponse(BaseModel):
    message: str
    provider_id: int
    approval_status: str