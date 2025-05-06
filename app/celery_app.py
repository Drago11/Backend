from celery import Celery

from app.core.config import Settings


def make_celery(app_settings: Settings) -> Celery:
    return Celery(
        "worker",
        broker=app_settings.CELERY_BROKER_URL,
        backend=app_settings.CELERY_BACKEND_URL,
    )