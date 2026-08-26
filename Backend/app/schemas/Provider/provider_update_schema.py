from pydantic import BaseModel, Field


class ProviderUpdate(BaseModel):
    business_name: str = Field(
        min_length=2,
        max_length=100
    )

    business_address: str = Field(
        min_length=5,
        max_length=255
    )

    contact: str = Field(
        min_length=10,
        max_length=15
    )


class ProviderUpdateResponse(BaseModel):
    message: str