import random
import resend
from app.core.config import settings

resend.api_key = settings.resend_api_key

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def send_otp_email(to_email: str, otp: str):
    subject = "DocuMind - Your Verification Code"
    body = f"Your verification code is: {otp}\n\nThis code expires in 10 minutes."

    resend.Emails.send({
        "from": "DocuMind <onboarding@resend.dev>",
        "to": [to_email],
        "subject": subject,
        "text": body,
    })