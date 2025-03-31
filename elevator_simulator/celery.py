import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevator_simulator.settings')

app = Celery('elevator_simulator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()