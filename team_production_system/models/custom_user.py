import random

from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .notification_settings import NotificationSettings


# Model for all users
class CustomUser(AbstractUser):
    is_mentor = models.BooleanField(default=False)
    is_mentee = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    email = models.EmailField(max_length=75, unique=True)
    phone_number = PhoneNumberField(
        null=True, blank=True, unique=True, default=None)
    profile_photo = models.ImageField(
        upload_to='profile_photo', blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Check if user is a new user
        is_new_user = self.pk is None
        self.username = self.username.lower()
        super().save(*args, **kwargs)

        if is_new_user:
            # Instantiate notification model for new user
            NotificationSettings.objects.create(user=self)
            # Assign default photo to a new user
            self.get_default_photo()
            self.save()

    def get_default_photo(self):
        files = default_storage.listdir('random_photo')[1]
        filename = random.choice(files)

        with default_storage.open(f'random_photo/{filename}') as file:
            self.profile_photo.save(filename, file, save=False)
