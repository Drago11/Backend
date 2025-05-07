import logging

from fastapi import HTTPException
from jinja2 import FileSystemLoader, Environment
from pydantic import EmailStr

from ..core import send_email_async

logger = logging.getLogger("uvicorn")

env = Environment(
    loader=FileSystemLoader(
        "app/templates"
    ),
    enable_async=True,
)

email_verify_template =env.get_template("UserInfoTemplate.html")

async def get_email_verification_template(**kwargs) -> str:
    return await email_verify_template.render_async(**kwargs)

async def send_email_verification_email(
        subject: str,
        verification_code:str,
        body:str,
        recipient: list[EmailStr]
) -> None:
    try:
        rendered_body = await get_email_verification_template(title=verification_code, body=body)
        send_email_async.delay(
            subject=subject,
            recipients=recipient,
            body=rendered_body
        )

    except Exception as e:
        logger.error("Error occurred while sending email verification mail")
        logger.error(e)
        raise HTTPException(status_code=500, detail="An unknown error occurred")
