from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "campus_employment",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.notifications", "app.tasks.data_export"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_routes={
        "app.tasks.notifications.*": {"queue": "notifications"},
        "app.tasks.data_export.*": {"queue": "export"},
    },
    beat_schedule={
        "daily_backup": {
            "task": "app.tasks.data_export.daily_backup",
            "schedule": 86400.0,
        },
        "check_expired_jobs": {
            "task": "app.tasks.jobs.check_expired",
            "schedule": 3600.0,
        },
    }
)
