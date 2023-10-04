from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from team_production_system.serializers import (
    AvailabilitySerializer,
    AvailabilitySerializerV2
)
from team_production_system.models import Mentor, Availability


# V1 API #
# Create and view all availabilities
class AvailabilityListCreateView(generics.ListCreateAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the Mentor instance for the logged in user
        mentor = Mentor.objects.get(user=self.request.user)
        # Exclude any availability that has an end time in the past
        # and filter availabilities belonging to the logged in user's mentor
        return Availability.objects.filter(mentor=mentor,
                                           end_time__gte=timezone.now()
                                           ).select_related('mentor__user')


# V2 API #
# Create and view all availabilities
class AvailabilityListCreateViewV2(generics.ListCreateAPIView):
    serializer_class = AvailabilitySerializerV2
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the Mentor instance for the logged in user
        mentor = Mentor.objects.get(user=self.request.user)
        # Exclude any availability that has an end time in the past
        # and filter availabilities belonging to the logged in user's mentor
        return Availability.objects.filter(mentor=mentor,
                                           end_time__gte=timezone.now()
                                           ).select_related('mentor__user')
