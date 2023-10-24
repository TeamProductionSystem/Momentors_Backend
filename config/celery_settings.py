from __future__ import absolute_import
import os
import environ
import ssl
from celery import Celery
from django.conf import settings

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    USE_S3=(bool, False),
    RENDER=(bool, False)
)

environ.Env.read_env()

your_env = env('ENVIRONMENT')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

if your_env == 'prod':
    app = Celery(
        "config",
        broker_use_ssl={
            'ssl_cert_reqs': ssl.CERT_NONE
        },
        redis_backend_use_ssl={
            'ssl_cert_reqs': ssl.CERT_NONE
        }
    )
elif your_env == 'dev':
    app = Celery('config')
else:
    raise ValueError('ENVIRONMENT in .env file should be either "dev" or "prod".')

app.conf.beat_schedule = {
    'notify-every-5-min': {
        'task': 'team_production_system.tasks.notify',
        'schedule': 300.0,
    },
}

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
