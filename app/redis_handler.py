from typing import Optional, Annotated

from fastapi.params import Depends

from .core import get_app_settings, Settings
from redis.asyncio import Redis



class RedisClient:
    _instance: Optional[Redis] = None

    @classmethod
    def get_instance(cls, settings: Settings) -> Redis:
        if cls._instance is None:
            cls._instance = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        return cls._instance


def get_redis_client(settings: Annotated[Settings, Depends(get_app_settings)]) -> Redis:
    return RedisClient.get_instance(settings=settings)