from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Session
from rest_framework.response import Response
from rest_framework import status


@shared_task
# Redis will run this every 5 minutes
def notify(session_pk):
    now = datetime.now(timezone.utc)
    session = Session.objects.get(pk=session_pk)
    start_time = session.start_time

    # We check a range of times since the plan is to have Redis run every 5 minutes
    if start_time - timedelta(minutes=60) <= now <= start_time - timedelta(minutes=55):
        if session.mentor.user.notification_settings.sixty_minute_alert:
            session.sixty_min_notify()
    if start_time - timedelta(minutes=15) <= now <= start_time - timedelta(minutes=10):
        if session.mentor.user.notification_settings.fifteen_minute_alert:
            session.fifteen_min_notify()
