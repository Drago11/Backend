from typing import Annotated

from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db import get_db_session
from app.models import User
from app.schemas import UserOutModel, UserInModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_new_user(self, new_user: UserInModel) -> User:
        user = User(
            firstname=new_user.firstname,
            lastname=new_user.lastname,
            email=new_user.email,
            hashed_password = new_user.password
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_user_by_email(self, email:EmailStr) -> User:
        stmt = select(User).where(User.email == email)
        result= await self.session.execute(stmt)

        user: User = result.scalars().first()
        return user


def get_user_repo(session: Annotated[AsyncSession, Depends(get_db_session)]) -> UserRepository:
    return UserRepository(session)