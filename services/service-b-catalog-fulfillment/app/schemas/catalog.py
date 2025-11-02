"""Catalog schemas"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProductImageResponse(BaseModel):
    id: int
    url: str
    alt_text: Optional[str]
    is_primary: bool
    display_order: int
    
    class Config:
        from_attributes = True


class VariantResponse(BaseModel):
    id: int
    sku: str
    name: str
    price: float
    weight: float
    attributes: Optional[str]
    
    class Config:
        from_attributes = True


class VariantWithInventory(VariantResponse):
    available_quantity: int = 0


class ProductBase(BaseModel):
    name: str
    slug: str
    description: Optional[str]
    base_price: float
    category_id: int
    is_active: bool = True
    featured: bool = False


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[float] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None
    featured: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    images: List[ProductImageResponse] = []
    variants: List[VariantResponse] = []
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    id: int
    name: str
    slug: str
    base_price: float
    featured: bool
    category_id: int
    primary_image: Optional[str] = None
    
    class Config:
        from_attributes = True
