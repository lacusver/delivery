import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "delivery.settings")

app = Celery("delivery")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "change_car_location_every_3_minutes": {
        "task": "apps.service_delivery.tasks.update_car_location",
        "schedule": timedelta(minutes=3),
    },
}
