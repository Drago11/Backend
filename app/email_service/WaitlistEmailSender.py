import logging

from fastapi import BackgroundTasks
from jinja2 import FileSystemLoader, Environment
from pydantic import EmailStr

from app.email_service.send_email import send_email
from app.services import WaitlistService

logger = logging.getLogger("uvicorn")

env = Environment(
    loader=FileSystemLoader(
        "C:/Users/Adedara/OneDrive/Personal Work/kjbackend/app/templates"
    ),
    enable_async=True,
)

WaitlistTemplate = env.get_template("WaitlistTemplate.html")


async def render_waitlist_template(**kwargs) -> str:
    """Render the waitlist template with the given context variables."""
    return await WaitlistTemplate.render_async(**kwargs)


async def send_waitlist_confirmation_email(email: EmailStr, background_tasks: BackgroundTasks) -> None:
    """Send waitlist confirmation email to recipient"""
    try:
        body = await render_waitlist_template()

        background_tasks.add_task(
            send_email,
            subject="Welcome! - Knot9ja Waitlist Subscription Added",
            recipients=[email],
            body=body
        )
        # await send_email(
        # subject = "Welcome! - Knot9ja Waitlist Subscription Added",
        # recipients = [email],
        # body = body
        # )
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise Exception("Error creating email message")

async def add_email_to_waitlist(
        email: EmailStr,
        background_tasks: BackgroundTasks,
        waitlist_service: WaitlistService
):
    try:
        await send_waitlist_confirmation_email(email, background_tasks)
        await waitlist_service.add_email_to_waitlist(email)
    except:
        raise

