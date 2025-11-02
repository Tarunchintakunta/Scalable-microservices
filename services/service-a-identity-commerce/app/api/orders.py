"""Orders management routes"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.deps import get_db, get_current_user, get_current_admin
from app.models.user import User
from app.models.order import Order, OrderStatus
from app.schemas.order import OrderResponse, OrderStatusUpdate
from app.api.checkout import notify_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=List[OrderResponse])
def list_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all orders for current user"""
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get order details"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    return order


@router.post("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update order status (admin only)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    # Validate status transition
    valid_statuses = ["created", "paid", "packed", "shipped", "delivered", "cancelled"]
    if status_data.status not in valid_statuses:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
    
    old_status = order.status
    order.status = OrderStatus(status_data.status)
    
    # Update timestamps
    if status_data.status == "shipped":
        order.shipped_at = datetime.utcnow()
        # Send notification
        background_tasks.add_task(
            notify_service,
            "ORDER_SHIPPED",
            {"order_id": order.id, "order_number": order.order_number}
        )
    elif status_data.status == "delivered":
        order.delivered_at = datetime.utcnow()
    
    db.commit()
    db.refresh(order)
    
    return order


@router.get("/admin/all", response_model=List[OrderResponse])
def list_all_orders(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all orders (admin only)"""
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    return orders
