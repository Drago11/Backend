from typing import Annotated

from fastapi import BackgroundTasks, APIRouter, Depends
from pydantic import EmailStr

from app.email_service.WaitlistEmailSender import add_email_to_waitlist
from app.services import WaitlistService, get_waitlist_service

waitlist_router = APIRouter(tags=["Waitlist Router"])


@waitlist_router.post("/waitlist")
async def add_to_waitlist(
        email: EmailStr,
        background_tasks: BackgroundTasks,
        waitlist_service: Annotated[WaitlistService, Depends(get_waitlist_service)]
) -> dict[str, str]:
    print(waitlist_service)
    response = await add_email_to_waitlist(email, background_tasks, waitlist_service)
    return response
