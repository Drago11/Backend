import json
import logging
import random
from typing import Annotated

from argon2 import PasswordHasher
from fastapi import HTTPException
from fastapi.params import Depends
from pydantic import EmailStr
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError

from ..email_service.user_registration_email_sender import send_email_verification_email
from ..redis_handler import get_redis_client
from ..repositories import get_user_repo, UserRepository
from ..schemas import UserOutModel, UserInModel

logger = logging.getLogger("uvicorn")


class UserService:
    def __init__(self, user_repo: UserRepository, redis_client: Redis):
        self.repo = user_repo
        self.redis = redis_client

    async def verify_user(self, new_user: UserInModel) -> dict[str, str]:
        """This is creating a user in disguise: and the `create_user` function, doing the job of verifying.
        They were name-switched because of implementation"""
        existing_user = await self.get_user_by_email(new_user.email)
        if existing_user:
            raise HTTPException(status_code=409, detail="user already exists")

        # Hash passwords before they are even stored in redis
        ph = PasswordHasher()
        new_user.password = ph.hash(password=new_user.password)

        try:
            verification_code: str = str(random.randint(100000, 999999))
            await self.redis.set(
                verification_code,
                new_user.model_dump_json()  # Converting pydantic model to JSON
            )

            await send_email_verification_email(
                subject="Verify your email",
                verification_code=verification_code,
                body="Please use this code to verify your email",
                recipient=[new_user.email]
            )
            return {"detail": "verification code sent to the user's email"}
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise HTTPException(status_code=500, detail="error creating user")

    async def create_user(self, verification_code: str) -> UserOutModel:
        """This is verifying a user in disguise: and the `verify` function, doing the job of creating.
                They were name-switched because of implementation"""

        if not await self.redis.exists(verification_code):
            raise HTTPException(status_code=401, detail="verification code is invalid or has expired")

        try:
            user_data = UserInModel.from_dict(json.loads(await self.redis.get(verification_code)))

            created_user = await self.repo.create_new_user(user_data)

            await self.redis.delete(verification_code)  # Delete once user has been verified
            return UserOutModel.from_user(created_user)

        except IntegrityError:
            raise HTTPException(status_code=409, detail="user already exists")
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="an unknown error occurred")

    async def get_user_by_email(self, email: EmailStr) -> UserOutModel | None:
        try:
            user = await self.repo.get_user_by_email(email)
            if not user:
                return None
            return UserOutModel.from_user(user)

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")


def get_user_service(
        user_repo: Annotated[UserRepository, Depends(get_user_repo)],
        redis_client: Annotated[Redis, Depends(get_redis_client)]
) -> UserService:
    return UserService(user_repo, redis_client)
