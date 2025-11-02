"""SMS provider stub (logs instead of sending)"""


def send_sms(to: str, message: str):
    """
    Stub SMS sender - logs instead of actually sending
    In production, integrate with Twilio, AWS SNS, etc.
    """
    print(f"\n📱 SMS (Stub)")
    print(f"To: {to}")
    print(f"Message: {message}")
    print()
