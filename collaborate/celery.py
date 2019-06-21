import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collaborate.settings')

app = Celery('collaborate', broker='redis://localhost')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
