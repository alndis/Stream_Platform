# tasks.py
from celery import Celery
from fastapi_mail import FastMail, MessageSchema
from email_config import conf
import asyncio
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("celery")

celery = Celery("tasks", broker="redis://redis:6379/0")

import logging

logger = logging.getLogger("celery")

@celery.task
def send_confirmation_email(email: str, token: str):
    async def send_email():
        try:
            message = MessageSchema(
                subject="Email Confirmation",
                recipients=[email],
                body=f"Please confirm your email by clicking the following link: http://176.123.167.118:8000/api/auth/confirm/{token}",
                subtype="html"
            )
            fm = FastMail(conf)
            await fm.send_message(message)
            logger.info(f"Email sent to {email}")
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {e}")
            raise

    asyncio.run(send_email())
