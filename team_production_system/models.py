from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from datetime import datetime, timedelta
from multiselectfield import MultiSelectField


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


# The mentor model that allows the mentor to select skills they know and information about them
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


# Model for mentees to input thier team
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

    def is_available(self):
        now = datetime.now()
        return self.end_time > now and True

    # Show a rolling 7 day calander to the mentor, so they can input their availabiltie
    def get_next_seven_days_availability(self):
        availabilities = []
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=7)
        slots = self.availabilities.filter(
            start_time__range=[start_date, end_date]).order_by('start_time')
        for current_day in range(start_date, end_date+timedelta(days=1)):
            availabilities.append(
                (current_day, slots.filter(start_time__date=current_day)))
        return availabilities

    # Check if the given time slot is available within this availability window.
    def is_slot_available(self, start_time, end_time):
        sessions = self.mentor_availability.mentor_session.filter(
            start_time__lt=end_time, end_time__gt=start_time)
        return not sessions.exists()


# A form for mentees to fill out information about what they need help with when setting up a session.
# This information will be sent to the mentor that the mentee is scheduling a session with
class SessionRequestForm(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='request')
    project = models.CharField(max_length=500)
    help_text = models.TextField(max_length=500)
    git_link = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)


# The session model allows the mentee to setup a session and allows both mentee and mentor see their sessions they have scheduled
class Session(models.Model):
    mentor_availability = models.ForeignKey(
        Availability, on_delete=models.CASCADE, related_name='mentor_session')
    mentee = models.ForeignKey(
        Mentee, on_delete=models.CASCADE, related_name='mentee_session')
    start_time = models.DateTimeField()
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

    def save(self, *args, **kwargs):
        if self.status == 'Confirmed':
            # The idea here is to update the status to 'Confirmed' only if the session has been confirmed by the mentor
            super(Session, self).save(*args, **kwargs)
        else:
            # Calculate the end time of the session
            self.end_time = self.start_time + \
                timedelta(minutes=self.session_length)
            # Check if the requested slot is available
            if self.mentor_availability.is_slot_available(self.start_time, self.end_time):
                # Slot is available, save the session
                self.status = 'Pending'
                super(Session, self).save(*args, **kwargs)
            else:
                # Slot is not available, raise an error
                raise ValueError('Requested time slot is not available')

    def __str__(self):
        return f"{self.mentor_availability.mentor.user.username} session with {self.mentee.user.username}"


# Notification model that will the mentor to be alerted when they have a session request. 
class Notification(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
