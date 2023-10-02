from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import datetime, timedelta
import boto3
from django.http import Http404
from .serializers import (
    AvailabilitySerializer,
    CustomUserSerializer,
    MenteeListSerializer,
    MenteeProfileSerializer,
    MentorListSerializer,
    MentorProfileSerializer,
    NotificationSettingsSerializer,
    SessionSerializer,
)
from .custom_permissions import (
    IsMentorMentee,
    IsOwnerOrAdmin,
    NotificationSettingsPermission,
)
from .models import (
    Availability,
    CustomUser,
    Mentee,
    Mentor,
    NotificationSettings,
    Session,
)


# View to update the user profile information
class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_object(self):
        user = self.request.user
        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            return user
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({
                'error': 'An unexpected error occurred.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        user = self.request.user

        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'is_mentor',
            'is_mentee',
            'is_active',
        ]

        for field in fields:
            if field in request.data:
                setattr(user, field, request.data[field])

        if 'profile_photo' in request.FILES:
            if user.profile_photo:
                s3 = boto3.client('s3')
                s3.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=user.profile_photo.name)

            user.profile_photo = request.FILES['profile_photo']

        user.save()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# View to see a list of all users flagged as a mentor
class MentorList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.filter(
        is_mentor=True
        ).select_related(
            "mentor"
        ).prefetch_related(
            "mentor__mentor_availability")
    serializer_class = MentorListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset:
            return Response({"message": "No mentors found."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MentorFilteredList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        skills = self.kwargs['skills'].split(',')
        queryset = Mentor.objects.filter(skills__icontains=skills[0])
        for skill in skills[1:]:
            queryset = queryset.filter(skills__icontains=skill)

        if not queryset.exists():
            return Response({"message": "No mentors found."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = MentorProfileSerializer(queryset, many=True)
        return Response(serializer.data)


# View to allow mentors to create and view the about me/skills.
class MentorInfoView(generics.ListCreateAPIView):
    serializer_class = MentorProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Mentor.objects.filter(user=self.request.user)


# View to edit the logged in mentors about me and skills
class MentorInfoUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MentorProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        return self.request.user.mentor


# View to see a list of all users flagged as a mentee
class MenteeList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            queryset = CustomUser.objects.filter(
                is_mentee=True).select_related("mentee")
        except Exception:
            return Response({"error": "Failed to retrieve mentee list."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not queryset.exists():
            return Response({"message": "No mentees found."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = MenteeListSerializer(queryset, many=True)
        response_data = serializer.data
        return Response(response_data)


# View to allow mentees to create and view the about me/skills.
class MenteeInfoView(generics.ListCreateAPIView):
    serializer_class = MenteeProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Mentee.objects.filter(user=self.request.user)


# View to edit the logged in mentees team number
class MenteeInfoUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenteeProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        return self.request.user.mentee


# Create and view all availabilities
class AvailabilityListCreateView(generics.ListCreateAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the Mentor instance for the logged in user
        mentor = Mentor.objects.get(user=self.request.user)
        # Exclude any availability that has an end time in the past
        # and filter availabilities belonging to the logged in user's mentor
        return Availability.objects.filter(
            mentor=mentor,
            end_time__gte=timezone.now(),
        ).select_related('mentor__user')


# Delete an availability
class AvailabilityDeleteView(generics.DestroyAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self):
        try:
            # Get the Availability instance for the logged in user
            availability = Availability.objects.select_related(
                'mentor__user').get(id=self.kwargs['pk'])
            self.check_object_permissions(self.request, availability)
            return availability
        except Availability.DoesNotExist:
            raise Http404("No Availability matches the given query.")


# Time conversion helper function
# During a session request, must convert start_time string to a datetime
# object in order to use timedelta to check for overlapping sessions

def time_convert(time, minutes):
    # Convert string from front end to datetime object
    datetime_obj = datetime.strptime(
        time,
        '%Y-%m-%dT%H:%M:%S.%fZ',
    ).replace(tzinfo=timezone.utc)
    # Change time dependent on session length minutes
    datetime_delta = datetime_obj - timedelta(minutes=minutes)
    # Convert datetime object back to string
    new_start_time = datetime.strftime(
        datetime_delta,
        '%Y-%m-%d %H:%M:%S%z',
    )[:-2]
    return new_start_time


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


class SessionRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsMentorMentee]

    # Update the session status
    def perform_update(self, serializer):
        session = serializer.instance
        status = self.request.data.get('status')

        # Notify users if session is canceled
        if status == 'Canceled':
            session.status = status
            session.save()

            # If mentee cancels session, check mentor notification
            if self.request.user.is_mentee and \
                    session.mentor.user.notification_settings.session_canceled:
                session.mentor_cancel_notify()

            # If mentor cancels session, check mentee notification

            elif self.request.user.is_mentor and \
                    session.mentee.user.notification_settings.session_canceled:
                session.mentee_cancel_notify()

        # Notify mentee when a mentor confirms session request
        elif status == 'Confirmed':
            session.status = status
            meeting_link = session.create_meeting_link()
            session.save()

            # Check mentee's notification settings before notifying
            if session.mentee.user.notification_settings.session_confirmed:
                session.mentee_confirm_notify(meeting_link)

            # Check mentor's notification settings before notifying
            if session.mentor.user.notification_settings.session_confirmed:
                session.mentor_confirm_notify(meeting_link)

        else:
            serializer.save()


class SessionView(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get sessions for the logged in user
        # Exclude sessions that have already ended and
        # order by sessions that are coming up next first.
        return Session.objects.filter(Q(mentor__user=self.request.user) |
                                      Q(mentee__user=self.request.user),
                                      start_time__gt=timezone.now()
                                      ).order_by('start_time')


# View to show mentor timeslots a mentee can sign up for
class SessionSignupListView(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter out completed sessions
        return Session.objects.exclude(status='Completed',
                                       start_time__lt=timezone.now() -
                                       timedelta(hours=24))


class ArchiveSessionView(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get sessions for the logged in user
        return Session.objects.filter(Q(mentor__user=self.request.user) |
                                      Q(mentee__user=self.request.user),
                                      end_time__lt=timezone.now())


class NotificationSettingsView(generics.RetrieveUpdateAPIView):
    queryset = NotificationSettings.objects.all()
    serializer_class = NotificationSettingsSerializer
    permission_classes = [NotificationSettingsPermission]
