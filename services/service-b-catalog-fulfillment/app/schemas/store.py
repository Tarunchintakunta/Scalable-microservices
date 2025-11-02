"""Store schemas"""
from pydantic import BaseModel
from typing import Optional


class StoreResponse(BaseModel):
    id: int
    name: str
    address: str
    city: str
    state: str
    postal_code: str
    country: str
    latitude: float
    longitude: float
    phone: Optional[str]
    email: Optional[str]
    is_active: bool
    distance_km: Optional[float] = None  # Calculated field for nearby queries
    
    class Config:
        from_attributes = True
