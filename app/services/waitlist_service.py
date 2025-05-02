import logging
from typing import Sequence, Annotated

from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from app.models import WaitlistSubscribers
from app.repositories.waitlist_repository import WaitlistRepository, get_waitlist_repo

logger = logging.getLogger("uvicorn")


class WaitlistService:
    def __init__(self, waitlist_repository: WaitlistRepository):
        self.repo = waitlist_repository

    async def add_email_to_waitlist(self, email: EmailStr) -> dict[str, str]:
        """

        :param email:
        :return:
        """
        try:
            await self.repo.add_email_to_waitlist(email)
            return {"detail": "added to waitlist successfully"}

        except IntegrityError as e:
            logger.error("Error adding email to waitlist")
            logger.error(e)
            raise HTTPException(status_code=409, detail="User already in waitlist")
        except Exception as e:
            logger.error(f"Error adding email to waitlist: {e}")
            raise HTTPException(status_code=500, detail="Unknown error occured")

    async def get_waitlist_subscribers(self, ) -> Sequence[WaitlistSubscribers]:
        try:
            waitlist_users = await self.repo.get_waitlist_subscribers()
            return waitlist_users
        except Exception as e:
            logger.error(f"Error getting list of waitlist subscribers: {e}")
            raise HTTPException(status_code=500, detail=f"Error getting list of waitlist subscribers")

async def get_waitlist_service(waitlist_repository: Annotated[WaitlistRepository, Depends(get_waitlist_repo)])-> WaitlistService:
    return WaitlistService(waitlist_repository)
