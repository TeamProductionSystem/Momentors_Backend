from datetime import timedelta
from unittest.mock import MagicMock

from django.test import TestCase
from django.utils import timezone

from ....models import Session
from ....tasks import notify


class NotifyTestCase(TestCase):
    def test_notify_sixty_min(self):
        # Create a mock session
        session = MagicMock()
        session.start_time = timezone.now() + timedelta(minutes=60)
        session.mentor.user.notification_settings.sixty_minute_alert = True

        # Create a MagicMock object for the Session.objects manager
        session_manager = MagicMock()

        # Set up the mock filter method to return a list of mock sessions
        session_manager.filter.return_value = [session]

        # Replace the Session.objects manager with the mock object
        Session.objects = session_manager

        # Call the notify function
        notify()

        # Check that the session's sixty_min_notify method was called
        session.sixty_min_notify.assert_called_once()

    def test_notify_fifteen_min(self):
        # Create a mock session
        session = MagicMock()
        session.start_time = timezone.now() + timedelta(minutes=15)
        session.mentor.user.notification_settings.fifteen_minute_alert = True

        # Create a MagicMock object for the Session.objects manager
        session_manager = MagicMock()

        # Set up the mock filter method to return a list of mock sessions
        session_manager.filter.return_value = [session]

        # Replace the Session.objects manager with the mock object
        Session.objects = session_manager

        # Call the notify function
        notify()

        # Check that the session's sixty_min_notify method was called
        session.fifteen_min_notify.assert_called_once()
