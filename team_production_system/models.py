from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.mail import send_mail
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from datetime import timedelta
from smtplib import SMTPRecipientsRefused


# Create your models here.

# Model for all users
class CustomUser(AbstractUser):
    is_mentor = models.BooleanField(default=False)
    is_mentee = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    email = models.EmailField(max_length=75, unique=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    profile_photo = models.ImageField(
        upload_to='profile_photo', blank=True, null=True)

    def __str__(self):
        return self.username


# The mentor model that allows the mentor to select skills
# they know and information about them
class Mentor(models.Model):

    SKILLS_CHOICES = [
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('JavaScript', 'JavaScript'),
        ('React', 'React'),
        ('Python', 'Python'),
        ('Django', 'Django'),
        ('Django REST', 'Django REST')
    ]

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    about_me = models.TextField(max_length=1000)
    skills = MultiSelectField(choices=SKILLS_CHOICES,
                              max_choices=7, max_length=52)

    def __str__(self):
        return self.user.username


# Model for mentees to input their team
class Mentee(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    team_number = models.IntegerField()

    def __str__(self):
        return self.user.username


# Allow mentors to set their avaliabiltiy
class Availability(models.Model):
    mentor = models.ForeignKey(
        Mentor, on_delete=models.CASCADE, related_name='mentor_availability')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.mentor} is available from {self.start_time} to {self.end_time}."


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
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    status_choices = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Canceled', 'Canceled'),
        ('Completed', 'Completed')
    ]
    # The mentee will be able to schedule a 30 minute or 60 mintue session.
    status = models.CharField(
        max_length=10, choices=status_choices, default='Pending')
    session_length_choices = [
        (30, '30 minutes'),
        (60, '60 minutes')
    ]
    session_length = models.IntegerField(
        choices=session_length_choices, default=30)

    def end_time(self):
        return self.start_time + timedelta(minutes=self.session_length)

    def __str__(self):
        return f"{self.mentor_availability.mentor.user.username} session with {self.mentee.user.username} is ({self.status})"

    def mentor_session_notify(self):
        session_time = self.start_time.strftime('%-I:%M %p')
        session_date = self.start_time.strftime('%A, %B %-d')

        send_mail(
            subject=(
                f'{self.mentee.user.first_name} {self.mentee.user.last_name} has requested your help'),
            message=(f'{self.mentee.user.first_name} {self.mentee.user.last_name} from Team {self.mentee.team_number} has requested a {self.session_length}-minute mentoring session with you at {session_time} EST on {session_date}.'),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.mentor.user.email],
            )

    def session_cancel_notify(self):
        session_time = self.start_time.strftime('%-I:%M %p')
        session_date = self.start_time.strftime('%A, %B %-d')

        send_mail(
            subject=(
                f'{self.mentee.user.first_name} {self.mentee.user.last_name} has canceled their session'),
            message=(f'{self.mentee.user.first_name} {self.mentee.user.last_name} from Team {self.mentee.team_number} has canceled their {self.session_length}-minute mentoring session with you at {session_time} EST on {session_date}.'),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.mentor.user.email, self.mentee.user.email]

        )


# Notification model that will the mentor to be alerted when
# they have a session request.
class Notification(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
