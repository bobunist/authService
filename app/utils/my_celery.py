from celery import Celery

from config import get_settings

settings = get_settings()

celery = Celery('tasks', broker=settings.redis_url)

celery.conf.update(
    include=['app.services.auth.celery_tasks']
)
