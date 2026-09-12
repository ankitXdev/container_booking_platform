from pydantic import BaseModel


class ProviderApprovalResponse(BaseModel):
    message: str
    provider_id: int
    approval_status: str
