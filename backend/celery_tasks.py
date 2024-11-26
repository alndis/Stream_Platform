# tasks.py
from celery import Celery
from fastapi_mail import FastMail, MessageSchema
from email_config import conf  # Import your FastMail configuration
import asyncio  # Import asyncio to run async functions

celery = Celery("tasks", broker="redis://redis:6379/0")  # Update if necessary

@celery.task
def send_confirmation_email(email: str, token: str):
    # Define an inner async function to send the email
    async def send_email():
        message = MessageSchema(
            subject="Email Confirmation",
            recipients=[email],  # list of recipients
            body=f"Please confirm your email by clicking the following link: http://176.123.167.118:8000/api/auth/confirm/{token}",
            subtype="html"
        )

        fm = FastMail(conf)
        await fm.send_message(message)

    # Run the async function in an event loop
    asyncio.run(send_email())
