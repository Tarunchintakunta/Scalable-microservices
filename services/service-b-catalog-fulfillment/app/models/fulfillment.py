"""Fulfillment model"""
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
import enum

from app.db.session import Base


class FulfillmentStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PACKED = "packed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


class Fulfillment(Base):
    __tablename__ = "fulfillments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False, unique=True, index=True)  # Reference to Service A
    order_number = Column(String, nullable=False)
    status = Column(Enum(FulfillmentStatus), default=FulfillmentStatus.PENDING)
    tracking_number = Column(String)
    carrier = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    shipped_at = Column(DateTime)
