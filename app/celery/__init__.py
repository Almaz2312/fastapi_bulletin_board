from celery import Celery

from app.config.settings import settings


def setup_celery():
    celery = Celery(
        settings.APP_NAME,
        backend=settings.CELERY_RESULT_BACKEND,
        broker=settings.CELERY_BROKER_URL,
    )
    celery.conf.update(app.config)
    return celery
