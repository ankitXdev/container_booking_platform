from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class RouteItem(BaseModel):
    origin: str
    destination: str


class ProviderDetailResponse(BaseModel):
    # Core identity fields
    provider_id: int
    business_name: str
    business_address: str
    contact: str
    email: str
    approval_status: str
    created_at: Optional[datetime] = None

    # Aggregated performance stats
    active_containers_count: int = 0
    total_containers_count: int = 0
    completed_bookings_count: int = 0
    total_cargo_handled_kg: float = 0.0
    serviced_routes: List[RouteItem] = []

    # Compliance / KYC
    compliance_verified: bool = False