import asyncio
import logging
import smtplib
from email.mime.text import MIMEText

from fastapi_mail import MessageSchema, MessageType, FastMail
from pydantic import EmailStr

from .config import conf, email_settings, settings
from .celery_app import make_celery

celery_app = make_celery(settings)

logger = logging.getLogger("uvicorn")

@celery_app.task
def send_email(
        subject: str,
        recipients: list[str],
        body: str,
) -> None:
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = email_settings.MAIL_FROM
    msg["To"] = recipients

    with smtplib.SMTP(email_settings.MAIL_SERVER, email_settings.MAIL_PORT) as server:
        server.starttls()
        server.login(email_settings.MAIL_USERNAME, email_settings.MAIL_PASSWORD)  # Use app password if MFA is enabled
        server.sendmail(email_settings.MAIL_FROM, recipients, msg.as_string())

    logger.info(f"Successfully sent waitlist email to {recipients}")

@celery_app.task
def send_email_async(subject: str, recipients: list[str], body: str) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    asyncio.run(fm.send_message(message))
    logger.info(f"Successfully sent waitlist email to {recipients}")

