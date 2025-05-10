import uuid
import zoneinfo
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from argon2 import PasswordHasher
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core import settings
from app.repositories import RefreshTokenRepo

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def password_is_correct(user_password: str, supplied_password: str) -> bool:
    ph = PasswordHasher()
    if ph.verify(user_password, supplied_password):
        return True
    return False

def generate_access_token(
        email: str,
        firstname: str,
        lastname: str,
        phone: str,
        profile_picture_url: str
) -> str:
    payload = {
        "sub": email,
        "firstname": firstname,
        "lastname": lastname,
        "phone": phone,
        "profile_picture_url": profile_picture_url,
        "exp": datetime.now() + timedelta(hours=2)
    }

    access_token: str = jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return access_token

async def generate_refresh_token(
        email: str,
        token_repo: RefreshTokenRepo
) -> tuple[str,str]:
    """
    This function takes the email, generates a long-lived jwt token that also contains
    the id of the refresh token, the creation time, and the expiry time.

    Also stores the newly generated token in the database

    :param token_repo:
    :param email:
    :return: token_identifier, refresh_token
    """
    #Make sure to delete any existing refresh_token for a user before generating a new one
    await token_repo.delete_existing_token(email)

    # new token id
    token_identifier = str(uuid.uuid4())
    created_at = datetime.now(zoneinfo.ZoneInfo("UTC"))

    payload: dict = {
        "sub": email,
        "jti": token_identifier,
        "iat": created_at,
        "exp": created_at + timedelta(days=7),
        "type": "refresh"
    }

    refresh_token = jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    #Make sure to store new token in database
    await token_repo.store_token(token_identifier, refresh_token, email)

    return token_identifier, refresh_token

def get_current_user(token: Annotated[str, Depends(oauth_scheme)]) -> dict[str, str | None | int] | None:
    """
    Gets its token parameter from a FastAPI Dependency that checks the request for an "Authorization" header
    :param token:
    :return: user_data: str
    """
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except:
        raise
