from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from team_production_system.models import Availability, Mentee, Session
from team_production_system.serializers import SessionSerializer


def time_convert(time, minutes):
    # Convert string from front end to datetime object
    datetime_obj = datetime.strptime(
        time, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
    # Change time dependent on session length minutes
    datetime_delta = datetime_obj - timedelta(minutes=minutes)
    # Convert datetime object back to string
    new_start_time = datetime.strftime(
        datetime_delta, '%Y-%m-%d %H:%M:%S%z')[:-2]
    return new_start_time
# Time conversion helper function
# During a session request, must convert start_time string to a datetime
# object in order to use timedelta to check for overlapping sessions


# Create and view all sessions
class SessionRequestView(generics.ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Get the mentor availability ID from the request data
        mentor_availability_id = self.request.data.get('mentor_availability')

        # Get the mentor availability instance
        mentor_availability = Availability.objects.get(
            id=mentor_availability_id)

        # Ensure no overlap between mentor or mentee's sessions
        mentor = mentor_availability.mentor

        mentee = Mentee.objects.get(user=self.request.user)

        start_time = self.request.data['start_time']
        session_length = self.request.data['session_length']

        if session_length == 30:
            new_start_time = time_convert(start_time, session_length)

            if Session.objects.filter(
                Q(mentor=mentor, start_time=start_time,
                  status__in=['Pending', 'Confirmed']) |
                Q(mentor=mentor, start_time=new_start_time,
                  session_length=60, status__in=['Pending', 'Confirmed'])
            ).exists():
                raise ValidationError(
                    'A session with this mentor is \
                     already scheduled during this time.')

            elif Session.objects.filter(
                Q(mentee=mentee, start_time=start_time,
                    status__in=['Pending', 'Confirmed']) |
                Q(mentee=mentee, start_time=new_start_time,
                  session_length=60, status__in=['Pending', 'Confirmed'])
            ).exists():
                raise ValidationError(
                    'A session with this mentee is \
                    already scheduled during this time.')

            # Set the mentor for the session
            else:
                serializer.save(mentor=mentor,
                                mentor_availability=mentor_availability,
                                mentee=mentee)

            # Email notification to the mentor
                session = serializer.instance
                if session.mentor.user.notification_settings.session_requested:
                    session.mentor_session_notify()

        if session_length == 60:
            before_start_time = time_convert(start_time, 30)
            after_start_time = time_convert(start_time, -30)

            if Session.objects.filter(
                Q(mentor=mentor, start_time=start_time,
                  status__in=['Pending', 'Confirmed']) |
                Q(mentor=mentor, start_time=before_start_time,
                  session_length=60, status__in=['Pending', 'Confirmed']) |
                Q(mentor=mentor, start_time=after_start_time,
                  status__in=['Pending', 'Confirmed'])
            ).exists():
                raise ValidationError(
                    'A session with this mentor is \
                    already scheduled during this time.')

            elif Session.objects.filter(
                Q(mentee=mentee, start_time=start_time,
                  status__in=['Pending', 'Confirmed']) |
                Q(mentee=mentee, start_time=before_start_time,
                  session_length=60, status__in=['Pending', 'Confirmed']) |
                Q(mentee=mentee, start_time=after_start_time,
                  status__in=['Pending', 'Confirmed'])
            ).exists():
                raise ValidationError(
                    'A session with this mentee is already \
                    scheduled during this time.')

            # Set the mentor for the session
            else:
                serializer.save(mentor=mentor,
                                mentor_availability=mentor_availability,
                                mentee=mentee)

                # Email notification to the mentor
                session = serializer.instance
                if session.mentor.user.notification_settings.session_requested:
                    session.mentor_session_notify()
