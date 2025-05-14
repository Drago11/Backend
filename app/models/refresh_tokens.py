import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now())
    user_email: Mapped[str] = mapped_column(String(50), ForeignKey("users.email"), nullable=False)
    token: Mapped[str] = mapped_column(String(1000), nullable=True)

    user = relationship("User", back_populates="refresh_tokens")