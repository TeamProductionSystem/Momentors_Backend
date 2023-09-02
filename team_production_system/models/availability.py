from .mentor import Mentor
from django.db.models.constraints import UniqueConstraint
from django.db import models

# Allow mentors to set their avaliabiltiy
class Availability(models.Model):
    mentor = models.ForeignKey(
        Mentor, on_delete=models.CASCADE, related_name='mentor_availability')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['mentor', 'start_time'], name='availability_constraint')
        ]

    def __str__(self):
        return f"{self.mentor} is available from {self.start_time} to {self.end_time}."
