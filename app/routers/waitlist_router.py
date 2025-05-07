from typing import Annotated

from fastapi import BackgroundTasks, APIRouter, Depends
from pydantic import EmailStr
from starlette.responses import JSONResponse

from app.auth.api_key_checker import check_api_key
from app.services import WaitlistService, get_waitlist_service

waitlist_router = APIRouter(tags=["Waitlist Router"])


@waitlist_router.post("/waitlist")
async def add_to_waitlist(
        email: EmailStr,
        waitlist_service: Annotated[WaitlistService, Depends(get_waitlist_service)]
) -> dict[str, str]:
    response = await waitlist_service.add_email_to_waitlist(email)
    return response

@waitlist_router.post("/update_waitlist")
async def send_email_to_waitlist(
        subject:str,
        body:str,
        title:str,
        waitlist_service: Annotated[WaitlistService, Depends(get_waitlist_service)],
) -> dict[str, str]:
    return await waitlist_service.send_mail_to_waitlist_subscribers(
        subject=subject,
        title=title,
        body=body,
    )
