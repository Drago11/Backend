import logging
from typing import Annotated

import httpx
import jwt
from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError
from pydantic import EmailStr
from starlette.requests import Request

from app.core import settings
from app.core.utils import password_is_correct, generate_access_token, generate_refresh_token
from app.models import User, RefreshToken
from app.repositories import UserRepository, get_user_repo, get_token_repo, RefreshTokenRepo
from app.schemas import UserInModel

logger = logging.getLogger("uvicorn")

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    authorize_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': "openid profile email https://www.googleapis.com/auth/user.phonenumbers.read"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration"
)


class InvalidTokenException(Exception):
    pass


async def get_user_phone_number(google_access_token: str) -> str|None:
    #TODO: Do actual implementation
    headers = {"Authorization": f"Bearer {google_access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://people.googleapis.com/v1/people/me?personFields=phoneNumbers",
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            if "phoneNumbers" in data and data["phoneNumbers"]:
                return data["phoneNumbers"][0].get("value")  # Return the first phone number
            else:
                return None  # No phone number found
        else:
            print(f"Error fetching phone number: {response.status_code} - {response.text}")
            return None


class AuthHandler:
    def __init__(self, user_repo: UserRepository, token_repo: RefreshTokenRepo):
        self.user_repo = user_repo
        self.token_repo = token_repo


    async def login(self, username: str, password: str):
        """
        Will take username and password using the PasswordRequestForm
        will verify if the user exists
        and will verify if the password (hashed) and username matches.

        Then, if the email entered was initially created with Google sign in, prompt them to either sign in with google

        :param username:
        :param password:

        :return: access_token, refresh_token
        """
        existing_user: User = await self.user_repo.get_user_by_email(username)
        if not existing_user:
            raise HTTPException(status_code=400, detail="user does not exist")

        if existing_user.signupoption == "google":
            return {"detail": "Seems like you signed up with Google. Click 'Sign in with Google' to sign in instead"}

        if not password_is_correct(existing_user.hashed_password, password):
            raise HTTPException(status_code=401, detail="invalid credentials")

        try:
            access_token = generate_access_token(
                existing_user.email,
                existing_user.firstname,
                existing_user.lastname,
                existing_user.phone,
                existing_user.profile_picture_url,
            )
            token_identifier, refresh_token = await generate_refresh_token(
                existing_user.email,
                self.token_repo
            )

            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}
        except Exception as e:
            logger.error(f"Error logging in user: {e}")
            raise HTTPException(status_code=500, detail="an error occurred while logging in the user")


    async def refresh(self, refresh_token: str):
        """
        Take a refresh token and verify -
            if it is in the database
            If the token is still valid,
        and then generate a new access token, as well as a new refresh token invalidating the old one in the process,
        and then return both to the user.

        :param refresh_token:
        :return: access_token, refresh_token
        """
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, settings.ALGORITHM)

            existing_token: RefreshToken = await self.token_repo.retrieve_refresh_token(payload["jti"])
            if not existing_token:
                raise InvalidTokenException()


            email: str = existing_token.user.email
            firstname: str = existing_token.user.firstname
            lastname: str = existing_token.user.lastname
            phone: str = existing_token.user.phone
            profile_picture_url: str = existing_token.user.profile_picture_url

            new_access_token = generate_access_token(
                email,
                firstname,
                lastname,
                phone,
                profile_picture_url
            )

            token_identifier, new_refresh_token = await generate_refresh_token(
                email, self.token_repo
            )


            return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "Bearer"}
        except ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Token expired. Login in again")
        except InvalidTokenException as e:
            logger.error(e)
            raise HTTPException(status_code=401, detail="invalid or expired refresh token")
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Error refreshing token")

    # Authentication with Google
    async def handle_google_callback(self, request:Request):
        """
        Handles "sign in with Google" option.

        User authorizes our app to access their details, and google responds with a token we can use to access their
        details.
        We use the access token from Google to get user details such as:
            - Full name, email, phone number and profile picture -
        and then create our own access and refresh tokens to give to the user client for normal authentication.

        :param request:
        :return: access token, refresh token
        """
        try:
            token = await oauth.google.authorize_access_token(request)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

        google_access_token = token.get("access_token")

        user_info = token.get("userinfo")

        email = user_info["email"]
        firstname = user_info["given_name"]
        lastname = user_info["family_name"]
        profile_picture_url = user_info["picture"]
        phone_number = await get_user_phone_number(google_access_token)

        existing_user: User = await self.user_repo.get_user_by_email(email)
        if not existing_user:
            new_user = await self.user_repo.create_new_user(
                UserInModel(
                    firstname=firstname,
                    lastname=lastname,
                    email=email,
                    phone=phone_number,
                    profile_picture_url=profile_picture_url,
                ),
                signupoption="google"
            )
            user_to_login = new_user
        else:
            # For existing users, will make sure their details are kept in sync with their Google account.
            # Especially useful for phone number and profile picture.
            await self.user_repo.update_user_details(
                email=email,
                firstname=firstname,
                lastname=lastname,
                profile_picture_url=profile_picture_url,
                phone=phone_number
            )
            user_to_login = existing_user

        access_token = generate_access_token(
            user_to_login.email,
            user_to_login.firstname,
            user_to_login.lastname,
            user_to_login.phone,
            user_to_login.profile_picture_url,
        )
        token_identifier, refresh_token = await generate_refresh_token(
            email,
            self.token_repo
        )
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}

    async def logout(self, email: str):
        await self.token_repo.delete_existing_token(email)
        return {"detail": "logged out successfully"}

def get_auth_handler(
        user_repo: Annotated[UserRepository, Depends(get_user_repo)],
        token_repo: Annotated[RefreshTokenRepo, Depends(get_token_repo)]
) -> AuthHandler:
    return AuthHandler(user_repo, token_repo)
