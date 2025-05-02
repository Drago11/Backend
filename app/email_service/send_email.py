import logging

from fastapi_mail import FastMail, MessageSchema
from pydantic import EmailStr

from ..core import get_email_configuration

logger = logging.getLogger("uvicorn")


async def send_email(
        subject: str,
        recipients: list[EmailStr],
        body: str,
) -> None:
    try:
        conf = get_email_configuration()

        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype="html",
        )
        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info(f"Successfully sent waitlist email to {recipients}")

    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise Exception("Error creating email message")
