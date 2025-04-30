import contextlib
from typing import AsyncIterator, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from ..core import get_app_settings

settings = get_app_settings()


class Base(DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}


engine = create_async_engine(url=settings.DATABASE_URL, echo=settings.ECHO_SQL)
SessionLocal = async_sessionmaker(bind=engine, autocommit=False, expire_on_commit=False)


@contextlib.asynccontextmanager
async def get_db_session() -> AsyncIterator[AsyncSession]:
    # Create a session and handle rollback in case of errors
    session = SessionLocal()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
