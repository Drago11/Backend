from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base

from datetime import datetime

class WaitlistSubscribers(Base):
    __tablename__ = "waitlist_subscribers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())
