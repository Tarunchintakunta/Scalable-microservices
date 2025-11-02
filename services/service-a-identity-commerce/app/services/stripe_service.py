"""Stripe payment service"""
import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent(amount: float, currency: str = "usd", metadata: dict = None):
    """Create a Stripe payment intent"""
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency=currency,
            metadata=metadata or {},
            automatic_payment_methods={"enabled": True},
        )
        return intent
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


def retrieve_payment_intent(payment_intent_id: str):
    """Retrieve a payment intent"""
    try:
        return stripe.PaymentIntent.retrieve(payment_intent_id)
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


def verify_webhook_signature(payload: bytes, sig_header: str) -> dict:
    """Verify Stripe webhook signature"""
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")
