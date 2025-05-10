from typing import Sequence, Annotated

from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db_session
from ..models import WaitlistSubscriber


class WaitlistRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_email_to_waitlist(self, email: EmailStr) -> str:
        waitlist_subscriber = WaitlistSubscriber(
            email=email
        )
        self.session.add(waitlist_subscriber)
        await self.session.commit()
        return "Added"

    async def get_waitlist_subscribers(self, ) -> Sequence[WaitlistSubscriber]:
        stmt = select(WaitlistSubscriber)
        result = await self.session.execute(stmt)

        subscribers = result.scalars().all()
        return subscribers


def get_waitlist_repo(session: Annotated[AsyncSession,Depends(get_db_session)]) -> WaitlistRepository:
    return WaitlistRepository(session)
