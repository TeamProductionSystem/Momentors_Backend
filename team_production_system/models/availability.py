from .mentor import Mentor
from django.db.models.constraints import UniqueConstraint
from django.db import models


# Allow mentors to set their avaliabiltiy
class Availability(models.Model):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Requested', 'Requested'),
        ('Confirmed', 'Confirmed'),
    ]

    mentor = models.ForeignKey(
        Mentor, on_delete=models.CASCADE, related_name='mentor_availability'
        )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Open'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['mentor', 'start_time'],
                name='availability_constraint',
                violation_error_message='Availability already exists.'
                )
        ]

    def __str__(self):
        return (
            f"{self.mentor} is available from "
            f"{self.start_time} to {self.end_time}."
        )
