from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from datetime import datetime, timedelta
from multiselectfield import MultiSelectField


# Create your models here.


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


class Mentee(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    team_number = models.IntegerField()

    def __str__(self):
        return self.user.username


class Availability(models.Model):
    mentor = models.ForeignKey(
        Mentor, on_delete=models.CASCADE, related_name='availability')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def is_available(self):
        now = datetime.now()
        return self.end_time > now and True

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


class SessionRequestForm(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='sessions')
    project = models.CharField(max_length=500)
    help_text = models.TextField(max_length=500)
    git_link = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)


class Session(models.Model):
    mentor_availability = models.ForeignKey(
        Availability, on_delete=models.CASCADE, related_name='appointments')
    mentee = models.ForeignKey(
        Mentee, on_delete=models.CASCADE, related_name='appointments')
    start_time = models.DateTimeField()
    status_choices = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Canceled', 'Canceled'),
        ('Completed', 'Completed')
    ]
    status = models.CharField(
        max_length=10, choices=status_choices, default='Pending')
    session_length_choices = [
        (30, '30 minutes'),
        (60, '60 minutes')
    ]
    session_length = models.IntegerField(
        choices=session_length_choices, default=30)

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.session_length)

    def __str__(self):
        return f"{self.mentor_availability.mentor.user.username} session with {self.mentee.user.username}"

    def save(self, *args, **kwargs):
        if self.status == 'Confirmed':
            # The idea here is to update the status to 'Confirmed' only if the session has been confirmed by the mentor
            super(Session, self).save(*args, **kwargs)
        else:
            # Or set the status to 'Pending' by default and save the session
            self.status = 'Pending'
            super(Session, self).save(*args, **kwargs)


class Notification(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
