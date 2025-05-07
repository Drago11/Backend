import asyncio

from fastapi_mail import MessageSchema, MessageType, FastMail
from pydantic import EmailStr

from . import get_email_connection_config
from .config import get_app_settings, get_email_configuration, EmailSettings

import logging

import smtplib
from email.mime.text import MIMEText

from ..celery_app import make_celery

settings = get_app_settings()

celery_app = make_celery(settings)

logger = logging.getLogger("uvicorn")

@celery_app.task
def send_email(
        subject: str,
        recipients: list[str],
        body: str,
) -> None:
    email_config: EmailSettings = get_email_configuration()
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = email_config.MAIL_FROM
    msg["To"] = recipients

    with smtplib.SMTP(email_config.MAIL_SERVER, email_config.MAIL_PORT) as server:
        server.starttls()
        server.login(email_config.MAIL_USERNAME, email_config.MAIL_PASSWORD)  # Use app password if MFA is enabled
        server.sendmail(email_config.MAIL_FROM, recipients, msg.as_string())

    logger.info(f"Successfully sent waitlist email to {recipients}")

@celery_app.task
def send_email_async(subject: str, recipients: list[EmailStr], body: str) -> None:
    conf = get_email_connection_config()

    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    asyncio.run(fm.send_message(message))
    logger.info(f"Successfully sent waitlist email to {recipients}")

