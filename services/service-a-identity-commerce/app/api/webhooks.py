"""Stripe webhook handler"""
from fastapi import APIRouter, Request, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import SessionLocal
from app.models.payment import Payment, PaymentStatus
from app.models.order import Order, OrderStatus
from app.services.stripe_service import verify_webhook_signature
from app.api.checkout import notify_service

router = APIRouter(prefix="/payments", tags=["webhooks"])


@router.post("/webhook")
async def stripe_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle Stripe webhooks"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not sig_header:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing signature")
    
    try:
        event = verify_webhook_signature(payload, sig_header)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    # Handle the event
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        
        db = SessionLocal()
        try:
            # Update payment status
            payment = db.query(Payment).filter(
                Payment.stripe_payment_intent_id == payment_intent["id"]
            ).first()
            
            if payment:
                payment.status = PaymentStatus.COMPLETED
                
                # Update order status
                order = db.query(Order).filter(Order.id == payment.order_id).first()
                if order:
                    order.status = OrderStatus.PAID
                    order.paid_at = datetime.utcnow()
                    
                    # Send notification
                    background_tasks.add_task(
                        notify_service,
                        "ORDER_PAID",
                        {"order_id": order.id, "order_number": order.order_number}
                    )
                
                db.commit()
        finally:
            db.close()
    
    elif event["type"] == "payment_intent.payment_failed":
        payment_intent = event["data"]["object"]
        
        db = SessionLocal()
        try:
            payment = db.query(Payment).filter(
                Payment.stripe_payment_intent_id == payment_intent["id"]
            ).first()
            
            if payment:
                payment.status = PaymentStatus.FAILED
                db.commit()
        finally:
            db.close()
    
    return {"status": "success"}
