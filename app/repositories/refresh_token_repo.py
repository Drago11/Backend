import datetime
from typing import Annotated

from fastapi.params import Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_db_session
from app.models import RefreshToken


class RefreshTokenRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def store_token(self,token_identifier:str, token: str, email: str) -> RefreshToken:
        new_refresh_token = RefreshToken(
            id=token_identifier,
            created_at=datetime.datetime.now(),
            user_email=email,
            token=token
        )
        self.session.add(new_refresh_token)
        await self.session.commit()

        return new_refresh_token

    async def retrieve_refresh_token(self, token_identifier: str) -> RefreshToken:
        stmt = select(RefreshToken).options(selectinload(RefreshToken.user)).where(RefreshToken.id == token_identifier)
        result = await self.session.execute(stmt)

        refresh_token = result.scalars().first()
        return refresh_token

    async def delete_existing_token(self, email: str) -> None:
        stmt = delete(RefreshToken).where(RefreshToken.user_email == email)
        await self.session.execute(stmt)

def get_token_repo(session: Annotated[AsyncSession, Depends(get_db_session)]) -> RefreshTokenRepo:
    return RefreshTokenRepo(session)
