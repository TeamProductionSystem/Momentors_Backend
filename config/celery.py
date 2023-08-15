from __future__ import absolute_import
import django
from django.conf import settings
import os
import ssl
from .celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# for production
app = Celery(
    "config",
    broker_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    },
    redis_backend_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    }
)

# for development
# app = Celery('config')

app.conf.beat_schedule = {
    'notify-every-5-min': {
        'task': 'team_production_system.tasks.notify',
        'schedule': 300.0,
    },
}

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
