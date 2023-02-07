from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(AbstractUser):
    is_mentor = models.BooleanField(default=False)
    is_mentee = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    email = models.EmailField(max_length=75)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    about_me = models.TextField(max_length=1000)


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
        User, on_delete=models.CASCADE, primary_key=True)
    skill = models.CharField(choices=skills, max_length=50)

    def __str__(self):
        return self.first_name


class Mentee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    team_number = models.IntegerField()

    def __str__(self):
        return self.first_name
