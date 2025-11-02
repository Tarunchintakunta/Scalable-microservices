"""Address management routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate, AddressResponse

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.get("", response_model=List[AddressResponse])
def list_addresses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all addresses for current user"""
    addresses = db.query(Address).filter(Address.user_id == current_user.id).all()
    return addresses


@router.post("", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(
    address_data: AddressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new address"""
    # If this is set as default, unset other defaults
    if address_data.is_default:
        db.query(Address).filter(Address.user_id == current_user.id).update({"is_default": False})
    
    new_address = Address(**address_data.model_dump(), user_id=current_user.id)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


@router.get("/{address_id}", response_model=AddressResponse)
def get_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific address"""
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    
    return address


@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    address_data: AddressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an address"""
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    
    # If setting as default, unset other defaults
    if address_data.is_default:
        db.query(Address).filter(
            Address.user_id == current_user.id,
            Address.id != address_id
        ).update({"is_default": False})
    
    for key, value in address_data.model_dump(exclude_unset=True).items():
        setattr(address, key, value)
    
    db.commit()
    db.refresh(address)
    return address


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an address"""
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    
    db.delete(address)
    db.commit()
    return None
