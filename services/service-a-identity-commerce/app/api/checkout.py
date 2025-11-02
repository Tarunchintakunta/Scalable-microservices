"""Checkout and payment routes"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import httpx
import json
from datetime import datetime

from app.core.deps import get_db, get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem, OrderStatus
from app.models.payment import Payment, PaymentStatus
from app.models.address import Address
from app.schemas.order import CheckoutRequest, PaymentIntentResponse, PaymentConfirmRequest, OrderResponse
from app.services.stripe_service import create_payment_intent, retrieve_payment_intent

router = APIRouter(prefix="/checkout", tags=["checkout"])


async def notify_service(event_type: str, data: dict):
    """Send notification to Service C"""
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                settings.NOTIFICATIONS_URL,
                json={"type": event_type, "data": data},
                timeout=5.0
            )
    except Exception as e:
        print(f"Failed to send notification: {e}")


@router.post("/create-payment-intent", response_model=PaymentIntentResponse)
async def create_checkout_payment_intent(
    checkout_data: CheckoutRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create payment intent and order"""
    # Get cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")
    
    # Get addresses
    shipping_address = db.query(Address).filter(
        Address.id == checkout_data.shipping_address_id,
        Address.user_id == current_user.id
    ).first()
    billing_address = db.query(Address).filter(
        Address.id == checkout_data.billing_address_id,
        Address.user_id == current_user.id
    ).first()
    
    if not shipping_address or not billing_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    
    # Calculate totals
    subtotal = sum(item.price * item.quantity for item in cart.items)
    tax = subtotal * 0.08  # 8% tax
    shipping_cost = 10.0  # Flat rate
    total = subtotal + tax + shipping_cost
    
    # Create order
    import random
    order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    
    new_order = Order(
        user_id=current_user.id,
        order_number=order_number,
        status=OrderStatus.CREATED,
        subtotal=subtotal,
        tax=tax,
        shipping_cost=shipping_cost,
        total=total,
        shipping_address=json.dumps({
            "street": shipping_address.street,
            "city": shipping_address.city,
            "state": shipping_address.state,
            "postal_code": shipping_address.postal_code,
            "country": shipping_address.country
        }),
        billing_address=json.dumps({
            "street": billing_address.street,
            "city": billing_address.city,
            "state": billing_address.state,
            "postal_code": billing_address.postal_code,
            "country": billing_address.country
        })
    )
    db.add(new_order)
    db.flush()
    
    # Create order items
    for cart_item in cart.items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=cart_item.product_id,
            variant_id=cart_item.variant_id,
            sku=cart_item.sku,
            product_name=f"Product {cart_item.product_id}",  # Should fetch from Service B
            quantity=cart_item.quantity,
            price=cart_item.price
        )
        db.add(order_item)
    
    # Create Stripe payment intent
    try:
        intent = create_payment_intent(
            amount=total,
            metadata={"order_id": new_order.id, "order_number": order_number}
        )
        
        # Create payment record
        payment = Payment(
            order_id=new_order.id,
            stripe_payment_intent_id=intent.id,
            amount=total,
            status=PaymentStatus.PENDING
        )
        db.add(payment)
        db.commit()
        
        # Send notification
        background_tasks.add_task(
            notify_service,
            "ORDER_PLACED",
            {"order_id": new_order.id, "order_number": order_number, "user_email": current_user.email}
        )
        
        return PaymentIntentResponse(
            client_secret=intent.client_secret,
            order_id=new_order.id
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/confirm", response_model=OrderResponse)
async def confirm_payment(
    confirm_data: PaymentConfirmRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Confirm payment and finalize order"""
    # Get payment
    payment = db.query(Payment).filter(
        Payment.stripe_payment_intent_id == confirm_data.payment_intent_id
    ).first()
    
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    
    # Verify payment with Stripe
    try:
        intent = retrieve_payment_intent(confirm_data.payment_intent_id)
        
        if intent.status == "succeeded":
            payment.status = PaymentStatus.COMPLETED
            order = db.query(Order).filter(Order.id == payment.order_id).first()
            order.status = OrderStatus.PAID
            order.paid_at = datetime.utcnow()
            
            # Clear cart
            cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
            if cart:
                db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
            
            db.commit()
            db.refresh(order)
            
            # Send notification
            background_tasks.add_task(
                notify_service,
                "ORDER_PAID",
                {"order_id": order.id, "order_number": order.order_number, "user_email": current_user.email}
            )
            
            return order
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment not successful: {intent.status}"
            )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
