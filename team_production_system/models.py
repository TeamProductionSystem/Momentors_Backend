from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True) 
    photo = models.ImageField(upload_to="user_photo", blank=True, null=True)
    employee_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.first_name