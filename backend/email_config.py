from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os
load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_USERNAME"),  # Use the same email as MAIL_USERNAME
    MAIL_PORT=587,
    MAIL_SERVER="smtp.mail.ru",  # Update to the correct SMTP server for your email provider
    MAIL_FROM_NAME="Stream Platform",
    MAIL_STARTTLS=True,            # Enable STARTTLS
    MAIL_SSL_TLS=False,            # Disable SSL/TLS
)
