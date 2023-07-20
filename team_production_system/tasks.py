from celery import shared_task
from datetime import datetime
from .models import Session


@shared_task
# Redis will run this every 5 (?) minutes
def notify(session_id):
    start_time = session_id.start_time
    now = datetime.datetime.now()
    session = Session.objects.get(id=session_id)

    # We may need to mess with the logic if the server only runs every 5 min to check
    if now == start_time - datetime.timedelta(minutes=60):
        if session.user.notification_settings.sixty_minute_alert:
            session.sixty_min_notify()
    if now == start_time - datetime.timedelta(minutes=15):
        # check spelling of alert
        if session.user.notification_settings.fifteen_minute_alert:
            session.fifteen_min_notify()
