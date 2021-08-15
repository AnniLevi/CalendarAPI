import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CalendarAPI.settings')

app = Celery('CalendarAPI')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
