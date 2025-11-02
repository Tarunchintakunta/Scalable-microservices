"""Review schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReviewCreate(BaseModel):
    product_id: int
    rating: int  # 1-5
    title: Optional[str] = None
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    title: Optional[str]
    comment: Optional[str]
    verified_purchase: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
