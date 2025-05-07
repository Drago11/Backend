from aiosmtplib import email
from pydantic import BaseModel, EmailStr

from app.models import User

class UserInModel(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str

class UserOutModel(BaseModel):
    firstname: str
    lastname: str
    email: str
    profile_picture_url: str

    @classmethod
    def from_user(cls, user_data: User) -> "UserOutModel":
        return UserOutModel(
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            email=user_data.email,
            profile_picture_url=user_data.profile_picture_url
        )