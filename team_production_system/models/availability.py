from .mentor import Mentor
from django.db.models.constraints import UniqueConstraint
from django.db import models
from datetime import timedelta


# Allow mentors to set their avaliabiltiy
class Availability(models.Model):
    mentor = models.ForeignKey(
        Mentor, on_delete=models.CASCADE, related_name='mentor_availability')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['mentor', 'start_time'],
                name='availability_constraint')
        ]

    def __str__(self):
        return (
            f"{self.mentor} is available from "
            f"{self.start_time} to {self.end_time}."
        )

    def save(self, *args, **kwargs):
            all_availabilities = []

            # Create a list of all availabilities in 30 minute increments
            while self.start_time < self.end_time:
                all_availabilities.append(
                    Availability(
                        mentor=self.mentor,
                        start_time=self.start_time,
                        end_time=self.start_time + timedelta(minutes=30)
                    )
                )
                self.start_time += timedelta(minutes=30)
            
            # Bulk create all availabilities
            Availability.objects.bulk_create(all_availabilities)