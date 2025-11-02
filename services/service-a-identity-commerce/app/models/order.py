"""Order and OrderItem models"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.session import Base


class OrderStatus(str, enum.Enum):
    CREATED = "created"
    PAID = "paid"
    PACKED = "packed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_number = Column(String, unique=True, index=True, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED, nullable=False)
    
    # Amounts
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, default=0.0)
    shipping_cost = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    
    # Addresses (snapshot)
    shipping_address = Column(Text, nullable=False)
    billing_address = Column(Text, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False, cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    variant_id = Column(Integer, nullable=True)
    sku = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
