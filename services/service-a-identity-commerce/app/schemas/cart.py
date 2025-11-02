"""Cart schemas"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CartItemBase(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    sku: str
    quantity: int = 1
    price: float


class CartItemCreate(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    sku: str
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemResponse(CartItemBase):
    id: int
    cart_id: int
    
    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    items: List[CartItemResponse] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
