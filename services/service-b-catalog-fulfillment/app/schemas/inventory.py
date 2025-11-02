"""Inventory schemas"""
from pydantic import BaseModel
from typing import List


class InventoryResponse(BaseModel):
    variant_id: int
    sku: str
    quantity: int
    reserved: int
    available: int
    
    class Config:
        from_attributes = True


class ReserveInventoryItem(BaseModel):
    sku: str
    quantity: int


class ReserveInventoryRequest(BaseModel):
    items: List[ReserveInventoryItem]
    order_id: int


class ReserveInventoryResponse(BaseModel):
    success: bool
    reservation_id: Optional[int] = None
    message: str


class CommitInventoryRequest(BaseModel):
    order_id: int


class ReleaseInventoryRequest(BaseModel):
    order_id: int
