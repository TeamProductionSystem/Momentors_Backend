from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class CustomUser(AbstractUser):
    is_mentor = models.BooleanField(default=False)
    is_mentee = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    email = models.EmailField(max_length=75, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    profile_photo = models.ImageField(
        upload_to='profile_photo', blank=True, null=True)

    def __str__(self):
        return self.username


class Mentor(models.Model):

    skills = [
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
    skill = models.CharField(choices=skills, max_length=50)

    def __str__(self):
        return self.user.username


class Mentee(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    team_number = models.IntegerField()

    def __str__(self):
        return self.user.username


class SessionRequestForm(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='sessions')
    project = models.CharField(max_length=500)
    help_text = models.TextField(max_length=5000)
    git_link = models.URLField(max_length=200)
