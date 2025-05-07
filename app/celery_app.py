from celery import Celery

from app.core.config import Settings


def make_celery(app_settings: Settings) -> Celery:
    return Celery(
        "worker",
        broker=app_settings.REDIS_URL,
        backend=app_settings.REDIS_URL,
    )