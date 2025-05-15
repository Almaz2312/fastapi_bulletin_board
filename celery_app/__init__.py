from celery import Celery
from celery.schedules import crontab

from app.config.settings import settings


def setup_celery():
    celery = Celery(
        settings.PROJECT_NAME,
        backend=settings.CELERY_RESULT_BACKEND,
        broker=settings.CELERY_BROKER_URL,
    )

    return celery


celery_app = setup_celery()
celery_app.autodiscover_tasks(["app.celery_app"])

celery_app.conf.beat_schedule = {
    "flush_adn_save_redis_data": {
        "task": "app.celery_app.tasks.update_ads_views",
        "schedule": crontab()
    }
}
