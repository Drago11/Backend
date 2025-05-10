from typing import Annotated

from authlib.integrations.starlette_client import OAuth
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.requests import Request

from app.auth import AuthHandler, get_auth_handler, oauth
from app.core.utils import get_current_user

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/token")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_handler: Annotated[AuthHandler, Depends(get_auth_handler)]
):
    username, password = form_data.username, form_data.password
    tokens = await auth_handler.login(username, password)
    return tokens

@auth_router.post("/refresh")
async def refresh(
        refresh_token: str,
        auth_handler: Annotated[AuthHandler, Depends(get_auth_handler)]
):
    tokens = await auth_handler.refresh(refresh_token)
    return tokens

@auth_router.get("/google")
async def login_with_google(request: Request):
    """
    Doesn't take any user credentials. Instead, takes the request object
    (injected by FastAPI), and redirects the user to google's auth server

    :param request:
    :return: A redirection basically
    """
    redirect_uri= request.url_for("auth_google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@auth_router.get("/google/callback", name="auth_google_callback")
async def handle_google_callback(
    request: Request,
    auth_handler: Annotated[AuthHandler, Depends(get_auth_handler)]
):
    """
    The endpoint that google's authentication server calls back.
    The endpoint is supplied the `request` object which I then forward to google to help decode.
    It is from the decoded request that I get access to the users details which I can use to then create them or sign them in

    :param request:
    :param auth_handler:
    :return:
    """
    tokens = await auth_handler.handle_google_callback(request)

    return tokens

@auth_router.get("/get_user")
async def get_user(user_data: Annotated[dict, Depends(get_current_user)]):
    return user_data