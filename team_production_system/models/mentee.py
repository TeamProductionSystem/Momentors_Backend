from django.db import models

from .custom_user import CustomUser


# Model for mentees to input their team
class Mentee(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    team_number = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
