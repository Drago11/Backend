from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import EmailStr

from app.schemas.email_schema import EmailBody
from app.services import WaitlistService, get_waitlist_service

waitlist_router = APIRouter(tags=["Waitlist Router"])


@waitlist_router.post("/waitlist")
async def add_to_waitlist(
        email: EmailStr,
        waitlist_service: Annotated[WaitlistService, Depends(get_waitlist_service)],
        background_tasks: BackgroundTasks
) -> dict[str, str]:
    response = await waitlist_service.add_email_to_waitlist(email, background_tasks)
    return response

@waitlist_router.post("/update_waitlist")
async def send_email_to_waitlist(
        email_message: EmailBody,
        waitlist_service: Annotated[WaitlistService, Depends(get_waitlist_service)],
        background_tasks: BackgroundTasks
) -> dict[str, str]:
    return await waitlist_service.send_mail_to_waitlist_subscribers(
        email_message=email_message,
        background_tasks=background_tasks

    )
