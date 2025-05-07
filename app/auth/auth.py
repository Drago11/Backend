from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token")

auth_router = APIRouter()

def password_is_correct(username:str, password: str) -> bool:
    pass

@auth_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if password_is_correct(form_data.username, form_data.password):
        pass
