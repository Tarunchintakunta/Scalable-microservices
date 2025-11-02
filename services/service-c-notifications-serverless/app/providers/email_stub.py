"""Email provider stub (logs instead of sending)"""


def send_email(to: str, subject: str, body: str):
    """
    Stub email sender - logs instead of actually sending
    In production, integrate with SendGrid, AWS SES, etc.
    """
    print(f"\n📧 EMAIL (Stub)")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print()
