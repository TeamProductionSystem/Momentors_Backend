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


class Activities(models.Model):
    activity_name = models.TextField(max_length=250)
    activity_number = models.IntegerField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='activity_number')


    def __str__(self):
        return f'{self.activity_name}, {self.activity_number}'
