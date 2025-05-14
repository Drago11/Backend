from celery import Celery

from .config import Settings


def make_celery(app_settings: Settings) -> Celery:
    return Celery(
        "worker",
        broker=app_settings.CELERY_REDIS_URL,
        backend=app_settings.CELERY_REDIS_URL,
    )