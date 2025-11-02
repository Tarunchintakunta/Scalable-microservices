"""Review model"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, nullable=False)  # Reference to Service A
    rating = Column(Integer, nullable=False)  # 1-5
    title = Column(String)
    comment = Column(Text)
    verified_purchase = Column(Integer, default=0)  # Boolean as int
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="reviews")
