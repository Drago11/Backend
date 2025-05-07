from typing import Sequence, Annotated

from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db_session
from ..models.WaitlistSubscribers import WaitlistSubscribers


class WaitlistRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_email_to_waitlist(self, email: EmailStr) -> str:
        waitlist_subscriber = WaitlistSubscribers(
            email=email
        )
        self.session.add(waitlist_subscriber)
        await self.session.commit()
        await self.session.refresh(waitlist_subscriber)
        return "Added"

    async def get_waitlist_subscribers(self, ) -> Sequence[WaitlistSubscribers]:
        stmt = select(WaitlistSubscribers)
        result = await self.session.execute(stmt)

        subscribers = result.scalars().all()
        return subscribers


def get_waitlist_repo(session: Annotated[AsyncSession,Depends(get_db_session)]) -> WaitlistRepository:
    return WaitlistRepository(session)
