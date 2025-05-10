from datetime import datetime

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    firstname: Mapped[str] = mapped_column(String(64), nullable=False)
    lastname: Mapped[str] = mapped_column(String(64), nullable=False)
    email:Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)
    address_line1: Mapped[str] = mapped_column(String(255), nullable=True)
    address_line2: Mapped[str] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(20), nullable=True)
    state: Mapped[str] = mapped_column(String(20), nullable=True)
    country: Mapped[str] = mapped_column(String(64), nullable=True)
    bio: Mapped[str] = mapped_column(String(255), nullable=True)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    privacy_preference: Mapped[bool] = mapped_column(Boolean, default=True)
    profile_picture_url: Mapped[str] = mapped_column(String(255), nullable=True)
    signupoption: Mapped[str] = mapped_column(String(15), nullable=False)

    refresh_tokens = relationship("RefreshToken", back_populates="user")
