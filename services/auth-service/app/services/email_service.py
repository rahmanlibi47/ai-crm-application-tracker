import smtplib
from email.message import EmailMessage

from app.config import settings


def send_otp_email(to_email: str, otp: str):
    msg = EmailMessage()
    msg["Subject"] = "OTP from CareerLedger"
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg.set_content(f"Your OTP is: {otp}. It expires in 10 minutes.")

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        smtp.send_message(msg)


def send_login_otp_background(email: str, otp: str):
    print("BACKGROUND TASK STARTED", flush=True)

    try:
        send_otp_email(email, otp)
        print(f"OTP email sent successfully to {email}", flush=True)

    except Exception as e:
        print(f"OTP email failed for {email}: {e}", flush=True)