"""Cart management routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", response_model=CartResponse)
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's cart"""
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    
    if not cart:
        # Create new cart if doesn't exist
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    return cart


@router.post("/items", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item_data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    # Get or create cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    # Check if item already exists in cart
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.sku == item_data.sku
    ).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity += item_data.quantity
        db.commit()
    else:
        # TODO: Fetch price from Service B
        # For now, we'll need to pass price from frontend or fetch it
        new_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            variant_id=item_data.variant_id,
            sku=item_data.sku,
            quantity=item_data.quantity,
            price=0.0  # Should be fetched from Service B
        )
        db.add(new_item)
        db.commit()
    
    db.refresh(cart)
    return cart


@router.put("/items/{item_id}", response_model=CartResponse)
def update_cart_item(
    item_id: int,
    item_data: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    if item_data.quantity <= 0:
        db.delete(item)
    else:
        item.quantity = item_data.quantity
    
    db.commit()
    db.refresh(cart)
    return cart


@router.delete("/items/{item_id}", response_model=CartResponse)
def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    db.delete(item)
    db.commit()
    db.refresh(cart)
    return cart


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear all items from cart"""
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if cart:
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()
    return None
