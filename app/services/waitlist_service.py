import logging
from typing import Sequence, Annotated

from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from app.email_service.waitlist_email_sender import send_waitlist_confirmation_email, send_email_to_waitlist
from app.models import WaitlistSubscriber
from app.repositories.waitlist_repository import WaitlistRepository, get_waitlist_repo
from app.schemas.email_schema import EmailBody

logger = logging.getLogger("uvicorn")


class WaitlistService:
    def __init__(self, waitlist_repository: WaitlistRepository):
        self.repo = waitlist_repository

    async def add_email_to_waitlist(self, email: EmailStr) -> dict[str, str]:
        """
        Responsible for adding an email to the waitlist,
        as well as sending confirmation mails to the users: using the WaitlistEmailSender
        :param email:
        :return: dict[str, str]
        """
        try:
            await self.repo.add_email_to_waitlist(email)
            await send_waitlist_confirmation_email(email)
            return {"detail": "added to waitlist successfully"}

        except IntegrityError as e:
            logger.error("Error adding email to waitlist: User already in waitlist. See more error details below")
            logger.error(e)
            raise HTTPException(status_code=409, detail="User already in waitlist")
        except Exception as e:
            logger.error(f"Error adding email to waitlist: {e}")
            raise HTTPException(status_code=500, detail="Unknown error occured")

    async def get_waitlist_subscribers(self, ) -> Sequence[WaitlistSubscriber]:
        try:
            waitlist_users = await self.repo.get_waitlist_subscribers()
            return waitlist_users
        except Exception as e:
            logger.error(f"Error getting list of waitlist subscribers: {e}")
            raise HTTPException(status_code=500, detail=f"Error getting list of waitlist subscribers")

    async def send_mail_to_waitlist_subscribers(
            self,
            email_message: EmailBody
    ) -> dict[str, str]:
        try:
            waitlist_subs: Sequence[WaitlistSubscriber] = await self.get_waitlist_subscribers()
            waitlist_subs_emails: list[str] = [sub.email for sub in waitlist_subs]
            await send_email_to_waitlist(
                subject=email_message.subject,
                title=email_message.title,
                recipients=waitlist_subs_emails,
                body=email_message.body,
            )
            return {"detail": "successfully sent email to waitlist subscribers" }
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=500,
                detail="Error sending email to waitlist. Please try again"
            )

async def get_waitlist_service(waitlist_repository: Annotated[WaitlistRepository, Depends(get_waitlist_repo)])-> WaitlistService:
    return WaitlistService(waitlist_repository)
