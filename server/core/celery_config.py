# core/celery_config.py
import os

from celery import Celery


class CeleryConfig:
    broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]
    timezone = "UTC"
    enable_utc = True


celery_app = Celery("dental_portal")
celery_app.config_from_object(CeleryConfig)


def init_celery():
    celery_app.conf.update(
        task_routes={
            "tasks.*": {"queue": "tasks"},
        }
    )
    return celery_app
