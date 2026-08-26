from pydantic import BaseModel, Field


class ProviderSearch(BaseModel):
    business_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Business name or part of the business name to search for"
    )


class SearchResponse(BaseModel):
    provider_id: int
    business_name: str
    business_address: str | None = None
    contact: str | None = None
    email: str | None = None