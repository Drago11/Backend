import logging

from fastapi import HTTPException, BackgroundTasks
from jinja2 import FileSystemLoader, Environment
from pydantic import EmailStr

from ..core import send_email_async
from ..core.utils import render_waitlist_template, render_waitlist_update_template

logger = logging.getLogger("uvicorn")



async def send_waitlist_confirmation_email(email: EmailStr, background_tasks: BackgroundTasks) -> None:
    """Send waitlist confirmation email to recipient"""
    try:
        body = await render_waitlist_template()
        background_tasks.add_task(
            send_email_async,
            subject="Welcome! - Knot9ja Waitlist Subscription Added",
            recipients=[email],
            body=body
        )
        # send_email_async.delay(
        #     subject="Welcome! - Knot9ja Waitlist Subscription Added",
        #     recipients=[email],
        #     body=body
        # )

    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise


async def send_email_to_waitlist(
        subject: str,
        recipients: list[str],
        title: str,
        body: str,
        background_tasks: BackgroundTasks,
) -> None:
    try:
        rendered_body = await render_waitlist_update_template(title=title, body=body, email=recipients[0])

        for recipient in recipients:
            background_tasks.add_task(
                send_email_async,
                subject,
                [recipient],
                rendered_body
            )
            # send_email_async.delay(
            #     subject=subject,
            #     recipients=[recipient],
            #     body=rendered_body
            # )
    except Exception as e:
        logger.error(f"Error sending email to waitlist: {e}")
        raise HTTPException(status_code=500, detail="Error sending mail to waitlist")
