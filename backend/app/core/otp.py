import random
import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def send_otp_email(to_email: str, otp: str):
    subject = "DocuMind - Your Verification Code"
    body = f"Your verification code is: {otp}\n\nThis code expires in 10 minutes."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.smtp_email
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(settings.smtp_email, settings.smtp_password)
        server.sendmail(settings.smtp_email, to_email, msg.as_string())