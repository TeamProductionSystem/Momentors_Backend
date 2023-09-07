from django.db import models
from team_production_system.models import CustomUser


# Model for mentees to input their team
class Mentee(team_production_system.models.Mentee):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    team_number = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
