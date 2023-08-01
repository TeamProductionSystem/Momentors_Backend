from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Session


@shared_task
# Redis will run this every 5 (?) minutes
def notify(session_pk):
    now = datetime.now()
    session = Session.objects.get(pk=session_pk)
    start_time = session.start_time
    session.mentor_confirm_notify()

    # We may need to mess with the logic if the server only runs every 5 min to check
    if start_time - timedelta(minutes=60) <= now <= start_time - timedelta(minutes=55):
        if session.user.notification_settings.sixty_minute_alert:
            session.sixty_min_notify()
    if start_time - timedelta(minutes=15) <= now <= start_time - timedelta(minutes=10):
        if session.user.notification_settings.fifteen_minute_alert:
            session.fifteen_min_notify()
