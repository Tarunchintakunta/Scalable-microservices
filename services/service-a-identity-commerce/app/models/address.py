"""Address model"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.db.session import Base


class AddressType(str, enum.Enum):
    BILLING = "billing"
    SHIPPING = "shipping"
    BOTH = "both"


class Address(Base):
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address_type = Column(Enum(AddressType), default=AddressType.BOTH)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False, default="USA")
    is_default = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="addresses")
