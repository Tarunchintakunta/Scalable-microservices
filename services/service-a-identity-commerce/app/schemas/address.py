"""Address schemas"""
from pydantic import BaseModel
from typing import Optional


class AddressBase(BaseModel):
    address_type: str = "both"
    street: str
    city: str
    state: str
    postal_code: str
    country: str = "USA"
    is_default: bool = False


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    address_type: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    is_default: Optional[bool] = None


class AddressResponse(AddressBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True
