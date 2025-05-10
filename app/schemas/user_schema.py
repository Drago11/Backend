from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models import User


class UserInModel(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    phone: str|None
    password: str = None
    profile_picture_url: Optional[str|None] = None

    @classmethod
    def from_dict(cls, data: dict) -> "UserInModel":
        return cls(**data)


class UserOutModel(BaseModel):
    firstname: str
    lastname: str
    email: str
    phone: str
    profile_picture_url: str | None

    @classmethod
    def from_user(cls, user_data: User) -> "UserOutModel":
        return UserOutModel(
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            email=user_data.email,
            phone=user_data.phone,
            profile_picture_url=user_data.profile_picture_url
        )