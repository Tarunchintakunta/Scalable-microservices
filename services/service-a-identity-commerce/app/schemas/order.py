"""Order schemas"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    variant_id: Optional[int]
    sku: str
    product_name: str
    quantity: int
    price: float
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    order_number: str
    status: str
    subtotal: float
    tax: float
    shipping_cost: float
    total: float
    shipping_address: str
    billing_address: str
    created_at: datetime
    updated_at: datetime
    paid_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str


class CheckoutRequest(BaseModel):
    shipping_address_id: int
    billing_address_id: int


class PaymentIntentResponse(BaseModel):
    client_secret: str
    order_id: int


class PaymentConfirmRequest(BaseModel):
    payment_intent_id: str
