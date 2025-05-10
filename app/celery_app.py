from celery import Celery

from app.core.config import Settings


def make_celery(app_settings: Settings) -> Celery:
    return Celery(
        "worker",
        broker=f"{app_settings.REDIS_URL}/1",
        backend=f"{app_settings.REDIS_URL}/1",
    )