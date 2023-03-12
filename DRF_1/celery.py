import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF_1.settings')

app = Celery('DRF_1')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "pay_check_1_minut": {
        "task": "department.tasks.pay_check",
        "schedule": crontab(minute='*/1'),
    },
    "status_check_30_sec": {
        "task": "department.tasks.status_check",
        "schedule": crontab(minute='*/1')
    },
}

# @app.task(bind=True)
# def debug_task(self):
#    print(f'Request: {self.request!r}')