from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from app.auth.api_key_checker import check_api_key
from app.schemas import UserInModel
from app.services import UserService, get_user_service

user_router = APIRouter(dependencies=[Depends(check_api_key)], tags=["UserRouter"])

@user_router.post("/user")
async def create_new_user(user: UserInModel, user_service: Annotated[UserService, Depends(get_user_service)]):
    message = await user_service.verify_user(user)
    return message


@user_router.post("/verification-code/{code}")
async def verify_code(code: str, user_service: Annotated[UserService, Depends(get_user_service)]):
    message = await user_service.create_user(code)
    return message
