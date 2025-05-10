import logging
from typing import Annotated

from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.models import User
from app.schemas import UserInModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_new_user(self, new_user: UserInModel, signupoption: str = "email") -> User:
        user = User(
            firstname=new_user.firstname,
            lastname=new_user.lastname,
            email=new_user.email,
            phone=new_user.phone,
            hashed_password = new_user.password,
            signupoption=signupoption
        )

        self.session.add(user)
        await self.session.commit()

        return user

    async def get_user_by_email(self, email:str) -> User:
        stmt = select(User).where(User.email == email)
        result= await self.session.execute(stmt)

        user: User = result.scalars().first()
        return user

    async def update_user_details(self,email:str, **kwargs):
        stmt = (
            update(User)
            .where(User.email == email)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        result = await self.session.execute(stmt)
        await self.session.commit()

        #Log how many records were updated. Useful for checks
        logging.getLogger("uvicorn").info(f"Number of rows updated: {result.rowcount}")


def get_user_repo(session: Annotated[AsyncSession, Depends(get_db_session)]) -> UserRepository:
    return UserRepository(session)