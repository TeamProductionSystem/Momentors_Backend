from django.db import models
from django.contrib.auth.models import AbstractUser
from random import choice
import os.path
from os.path import isfile
from os.path import join as path_join
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from os import listdir


# Create your models here.

class Role(models.Model):
    MENTOR = 1
    MENTEE = 2
    STAFF = 3
    ROLE_CHOICES = (
        (MENTOR, 'mentor'),
        (MENTEE, 'mentee'),
        (STAFF, 'staff'),
    )

    role_id = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_role_id_display()


class User(AbstractUser):
    roles = models.ManyToManyField(Role)


def random_img():
    dir_path = os.path.join(
        settings.BASE_DIR, 'static/profile_pictures')
    files = [
        content for content in listdir(dir_path)
        if isfile(path_join(dir_path, content))]
    return choice(files)


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
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    email = models.EmailField(max_length=75)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    about_me = models.TextField(max_length=1000)
    photo = models.ImageField(upload_to="mentor_photo",
                              default=random_img(),)
    skill = models.CharField(choices=skills, max_length=50)

    def __str__(self):
        return self.first_name


class Mentee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=75)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    about_me = models.TextField(max_length=1000)
    team_number = models.IntegerField()
    photo = models.ImageField(upload_to="mentee_photo",
                              default=random_img(),)

    def __str__(self):
        return self.first_name
