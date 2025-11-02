"""Product and related models"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    slug = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text)
    base_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    variants = relationship("Variant", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")


class ProductImage(Base):
    __tablename__ = "product_images"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    url = Column(String, nullable=False)
    alt_text = Column(String)
    is_primary = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    
    # Relationships
    product = relationship("Product", back_populates="images")


class Variant(Base):
    __tablename__ = "variants"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    sku = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)  # e.g., "Small - Red"
    price = Column(Float, nullable=False)
    weight = Column(Float, default=0.0)  # in kg
    attributes = Column(Text)  # JSON string for size, color, etc.
    
    # Relationships
    product = relationship("Product", back_populates="variants")
    inventory = relationship("Inventory", back_populates="variant", uselist=False, cascade="all, delete-orphan")
