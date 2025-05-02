import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from ..core import get_app_settings

settings = get_app_settings()


class Base(DeclarativeBase):
    pass

engine = create_async_engine(url=settings.DATABASE_URL, echo=settings.ECHO_SQL)
SessionLocal = async_sessionmaker(bind=engine, autocommit=False, expire_on_commit=False)


async def get_db_session():
    async with SessionLocal() as session:
        yield session  # Automatically manages commit/rollback
