from pydantic import BaseModel


class ContainerAvailabilityUpdate(BaseModel):
    is_available: bool


class ContainerAvailabilityResponse(BaseModel):
    message: str
    is_available: bool
