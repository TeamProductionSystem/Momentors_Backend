# helper.py
# Purpose: Helper functions for the team_production_system app.

from datetime import timedelta
from django.utils import timezone
from team_production_system.models import Availability
from django.utils.dateparse import parse_datetime


# Create a list of Availability objects in 30 mins chunks for a time range
def create_30_min_availabilities(start_time_str, end_time_str, mentor):
    chunk_size = timedelta(minutes=30)
    start_time = parse_datetime(start_time_str)
    end_time = parse_datetime(end_time_str)

    availabilities = []
    while start_time < end_time:
        end_time_new = start_time + chunk_size
        if end_time_new > end_time:
            break
        availability = {
            'start_time': start_time,
            'end_time': end_time_new,
            'mentor': mentor.user.pk,
            'status': 'Open'
        }
        availabilities.append(availability)
        start_time += chunk_size
    return availabilities


# Check if the mentor has any overlapping availabilities
def is_overlapping_availabilities(mentor, data):
    """
    Check if there is any overlap with existing availabilities.
    """
    start_time = data['start_time']
    end_time = data['end_time']
    overlapping_availabilities = Availability.objects.filter(
        mentor=mentor,
        start_time__lt=end_time,
        end_time__gt=start_time
    )
    return overlapping_availabilities.exists()


# Check if the start_time is in the future
def is_valid_start_time(start_time):
    """
    Check that the start_time is in the future.
    """
    return start_time > timezone.now()


# Check if the end_time is after the start_time
def is_valid_end_time(start_time, end_time):
    """
    Check that the end_time is after the start_time.
    """
    return end_time > start_time
