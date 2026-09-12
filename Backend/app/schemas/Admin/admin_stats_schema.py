from pydantic import BaseModel


class ProviderStats(BaseModel):
    total: int
    pending: int
    approved: int
    rejected: int


class ContainerStats(BaseModel):
    total: int
    available: int
    unavailable: int


class BookingStats(BaseModel):
    total: int
    pending: int
    confirmed: int
    cancelled: int


class PlatformStatsResponse(BaseModel):
    total_users: int
    total_exporters: int
    total_providers: int
    providers: ProviderStats
    containers: ContainerStats
    bookings: BookingStats
    total_revenue: float
