import secrets
from datetime import timedelta

import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.db import models

from .availability import Availability
from .mentee import Mentee
from .mentor import Mentor


# The session model allows the mentee to setup a session and
# allows both mentee and mentor see their sessions they have scheduled
class Session(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE,
                               related_name='mentor_session')
    mentor_availability = models.ForeignKey(
        Availability, on_delete=models.CASCADE, related_name='mentor_session')
    mentee = models.ForeignKey(
        Mentee, on_delete=models.CASCADE, related_name='mentee_session')
    start_time = models.DateTimeField()
    project = models.CharField(max_length=500)
    help_text = models.TextField(max_length=500)
    git_link = models.URLField(max_length=200)
    confirmed = models.BooleanField(default=False)
    status_choices = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Canceled', 'Canceled'),
        ('Completed', 'Completed')
    ]
    # The mentee will be able to schedule a 30 minute or 60 minute session.
    status = models.CharField(
        max_length=10, choices=status_choices, default='Pending')
    session_length_choices = [
        (30, '30 minutes'),
        (60, '60 minutes')
    ]
    session_length = models.IntegerField(
        choices=session_length_choices, default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def end_time(self):
        return self.start_time + timedelta(minutes=self.session_length)

    def __str__(self):
        return (
            f"{self.mentor_availability.mentor.user.username} "
            f"session with {self.mentee.user.username} is ({self.status})"
        )

    # Notify a mentor that a mentee has requested a session
    def mentor_session_notify(self):
        # Define the timezone
        est = pytz.timezone('US/Eastern')

        # Convert the start time to EST
        est_start_time = self.start_time.astimezone(est)

        # Format the time and date
        session_time = est_start_time.strftime('%-I:%M %p')
        session_date = est_start_time.strftime('%A, %B %-d')

        send_mail(
            subject=(
                f'{self.mentee.user.first_name} {self.mentee.user.last_name} '
                f'has requested your help'
            ),
            message=(
                f'{self.mentee.user.first_name} {self.mentee.user.last_name} '
                f'from Team {self.mentee.team_number} '
                f'has requested a {self.session_length}-min mentoring session '
                f'with you at {session_time} EST on {session_date}.'
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.mentor.user.email],
        )

    # Create a a random string of characters to be used as a session code
    def create_session_code(self):
        # Set the start of the code to be 'MomentumMentorSession'
        code = 'MomentumMentorSession'
        # Append 20 random characters to the code
        code += secrets.token_urlsafe(20)
        return code

    # Create a jitsi meeting link for the session
    # with the randomly generated code
    def create_meeting_link(self):
        code = self.create_session_code()
        return f'https://meet.jit.si/{code}'

    # Notify the mentee and when the requested session has been confirmed
    def mentee_confirm_notify(self, meeting_link):
        # Define the timezone
        est = pytz.timezone('US/Eastern')

        # Convert the start time to EST
        est_start_time = self.start_time.astimezone(est)

        # Format the time and date
        session_time = est_start_time.strftime('%-I:%M %p')
        session_date = est_start_time.strftime('%A, %B %-d')

        send_mail(
            subject=('Mentor Session Confirmed'),
            message=(
                f'A session with {self.mentee.user.first_name} '
                f'and {self.mentor.user.first_name} '
                f'has been confirmed for a {self.session_length}'
                f'-minute mentoring session '
                f'at {session_time} EST on {session_date}. '
                f'Here is the link to your session: {meeting_link}'
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.mentee.user.email]
        )

    # Notify the mentor when the requested session has been confirmed
    def mentor_confirm_notify(self, meeting_link):
        # Define the timezone
        est = pytz.timezone('US/Eastern')

        # Convert the start time to EST
        est_start_time = self.start_time.astimezone(est)

        # Format the time and date
        session_time = est_start_time.strftime('%-I:%M %p')
        session_date = est_start_time.strftime('%A, %B %-d')

        send_mail(
            subject=('Mentor Session Confirmed'),
            message=(
                f'A session with {self.mentee.user.first_name} '
                f'and {self.mentor.user.first_name} '
                f'has been confirmed for a {self.session_length}'
                f'-minute mentoring session at {session_time} EST '
                f'on {session_date}. '
                f'Here is the link to your session: {meeting_link}'
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.mentor.user.email]
        )

    # Notify a mentor that a mentee has canceled a scheduled session
    def mentor_cancel_notify(self):
        # Define the timezone
        est = pytz.timezone('US/Eastern')

        # Convert the start time to EST
        est_start_time = self.start_time.astimezone(est)

        # Format the time and date
        session_time = est_start_time.strftime('%-I:%M %p')
        session_date = est_start_time.strftime('%A, %B %-d')

        send_mail(
            subject=(
                f'{self.mentee.user.first_name} {self.mentee.user.last_name} '
                f'has canceled their session'
            ),
            message=(
                f'{self.mentee.user.first_name} {self.mentee.user.last_name} '
                f'from Team {self.mentee.team_number} '
                f'has canceled their {self.session_length}'
                f'-minute mentoring session with you '
                f'at {session_time} EST on {session_date}.'
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.mentor.user.email],
        )

    # Notify a mentee that a mentor has canceled a scheduled session
    def mentee_cancel_notify(self):
        # Define the timezone
        est = pytz.timezone('US/Eastern')

        # Convert the start time to EST
        est_start_time = self.start_time.astimezone(est)

        # Format the time and date
        session_time = est_start_time.strftime('%-I:%M %p')
        session_date = est_start_time.strftime('%A, %B %-d')

        send_mail(
            subject=(
                f'{self.mentor.user.first_name} {self.mentor.user.last_name} '
                f'has canceled your session'
            ),
            message=(
                f'{self.mentor.user.first_name} {self.mentor.user.last_name} '
                f'has canceled the {self.session_length}'
                f'-minute mentoring session with you '
                f'at {session_time} EST on {session_date}.'
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.mentee.user.email],
        )

    # Notify a user that a session is coming up in 60 min
    # TODO: Needs unit testing
    def sixty_min_notify(self):
        # Define the timezone
        est = pytz.timezone('US/Eastern')

        # Convert the start time to EST
        est_start_time = self.start_time.astimezone(est)

        # Format the time and date
        session_time = est_start_time.strftime('%-I:%M %p')

        send_mail(
            subject=('Mentor Session in 60 Minutes'),
            message=(
                f'Your {self.session_length}-minute session with '
                f'{self.mentee.user.first_name} and '
                f'{self.mentor.user.first_name} '
                f'at {session_time} EST is coming up in 60 minutes.'
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.mentor.user.email, self.mentee.user.email],
        )

    # Notify a user that a session is coming up in 15 min
    # TODO: Needs unit testing
    def fifteen_min_notify(self):
        # Define the timezone
        est = pytz.timezone('US/Eastern')

        # Convert the start time to EST
        est_start_time = self.start_time.astimezone(est)

        # Format the time and date
        session_time = est_start_time.strftime('%-I:%M %p')

        send_mail(
            subject=('Mentor Session in 15 Minutes'),
            message=(
                f'Your {self.session_length}-minute session with '
                f'{self.mentee.user.first_name} and '
                f'{self.mentor.user.first_name} '
                f'at {session_time} EST is coming up in 15 minutes.'
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.mentor.user.email, self.mentee.user.email],
        )
