import logging

from fastapi import HTTPException
from jinja2 import FileSystemLoader, Environment
from pydantic import EmailStr

from ..core import send_email
from ..core.celery_utils import send_email_async

logger = logging.getLogger("uvicorn")

env = Environment(
    loader=FileSystemLoader(
        "app/templates"
    ),
    enable_async=True,
)

WaitlistTemplate = env.get_template("WaitlistTemplate.html")
WaitlistUpdateTemplate = env.get_template("UserInfoTemplate.html")


async def render_waitlist_template(**kwargs) -> str:
    """Render the waitlist template with the given context variables."""
    return await WaitlistTemplate.render_async(**kwargs)


async def render_waitlist_update_template(**kwargs) -> str:
    """Render the waitlist template with the given context variables."""
    return await WaitlistUpdateTemplate.render_async(**kwargs)


async def send_waitlist_confirmation_email(email: EmailStr) -> None:
    """Send waitlist confirmation email to recipient"""
    try:
        body = await render_waitlist_template()
        send_email_async.delay(
            subject="Welcome! - Knot9ja Waitlist Subscription Added",
            recipients=[email],
            body=body
        )

    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise


async def send_email_to_waitlist(
        subject: str,
        recipients: list[str],
        title: str,
        body: str,
) -> None:
    try:
        rendered_body = await render_waitlist_update_template(title=title, body=body)

        for recipient in recipients:
            send_email_async.delay(
                subject=subject,
                recipient=[recipient],
                body=rendered_body
            )
    except Exception as e:
        logger.error(f"Error sending email to waitlist: {e}")
        raise HTTPException(status_code=500, detail="Error sending mail to waitlist")
