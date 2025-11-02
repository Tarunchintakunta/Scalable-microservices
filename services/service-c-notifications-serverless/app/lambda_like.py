"""
Lambda-like handler for notifications
This function can be deployed to AWS Lambda in the future
"""
from typing import Dict
from app.providers.console_logger import log_notification
from app.providers.email_stub import send_email
from app.providers.sms_stub import send_sms
import os


def handle_event(event: Dict) -> Dict:
    """
    Handle notification events
    
    Args:
        event: Dict with structure:
            {
                "type": "ORDER_PLACED" | "ORDER_PAID" | "ORDER_SHIPPED" | "LOW_STOCK" | ...,
                "data": {...}
            }
    
    Returns:
        Dict with {"ok": True} or {"ok": False, "error": "..."}
    """
    try:
        event_type = event.get("type")
        data = event.get("data", {})
        
        # Always log to console
        log_notification(event_type, data)
        
        # Handle different event types
        if event_type == "ORDER_PLACED":
            handle_order_placed(data)
        elif event_type == "ORDER_PAID":
            handle_order_paid(data)
        elif event_type == "ORDER_SHIPPED":
            handle_order_shipped(data)
        elif event_type == "LOW_STOCK":
            handle_low_stock(data)
        else:
            print(f"⚠️  Unknown event type: {event_type}")
        
        return {"ok": True}
    
    except Exception as e:
        print(f"❌ Error handling event: {e}")
        return {"ok": False, "error": str(e)}


def handle_order_placed(data: Dict):
    """Handle ORDER_PLACED event"""
    order_id = data.get("order_id")
    order_number = data.get("order_number")
    user_email = data.get("user_email")
    
    if user_email:
        send_email(
            to=user_email,
            subject=f"Order Confirmation - {order_number}",
            body=f"Thank you for your order! Your order #{order_number} has been placed successfully."
        )


def handle_order_paid(data: Dict):
    """Handle ORDER_PAID event"""
    order_id = data.get("order_id")
    order_number = data.get("order_number")
    user_email = data.get("user_email")
    
    if user_email:
        send_email(
            to=user_email,
            subject=f"Payment Confirmed - {order_number}",
            body=f"Your payment for order #{order_number} has been confirmed. We're preparing your items for shipment."
        )


def handle_order_shipped(data: Dict):
    """Handle ORDER_SHIPPED event"""
    order_id = data.get("order_id")
    order_number = data.get("order_number")
    tracking_number = data.get("tracking_number", "N/A")
    
    # In production, fetch user email from Service A
    print(f"📦 Order {order_number} shipped. Tracking: {tracking_number}")
    
    # Optionally send SMS if enabled
    if os.getenv("ENABLE_SMS", "false").lower() == "true":
        phone = data.get("phone")
        if phone:
            send_sms(
                to=phone,
                message=f"Your order {order_number} has shipped! Track it: {tracking_number}"
            )


def handle_low_stock(data: Dict):
    """Handle LOW_STOCK event"""
    sku = data.get("sku")
    quantity = data.get("quantity")
    
    # Send alert to admin
    send_email(
        to=os.getenv("EMAIL_FROM", "admin@example.com"),
        subject=f"Low Stock Alert - {sku}",
        body=f"SKU {sku} is running low. Current quantity: {quantity}"
    )
