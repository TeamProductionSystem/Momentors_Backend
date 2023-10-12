from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import timedelta
from team_production_system.serializers import (
    AvailabilitySerializer,
    AvailabilitySerializerV2,
)
from silk.profiling.profiler import silk_profile
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
    permission_classes = [IsAuthenticated]
    serializer_class = AvailabilitySerializerV2


    def get_queryset(self):
        # Get the Mentor instance for the logged in user
        mentor = Mentor.objects.select_related('user').get(
            user=self.request.user)
        # Exclude any availability that has an end time in the past
        # and filter availabilities belonging to the logged in user's mentor
        return Availability.objects.filter(
            mentor=mentor, 
            end_time__gte=timezone.now() - timedelta(minutes=15)
            ).select_related('mentor__user')


    def create(self, request, *args, **kwargs):
        # Get the start time and end time from the request data
        start_time = parse_datetime(request.data['start_time'])
        end_time = parse_datetime(request.data['end_time'])
        # Create a list of Availability objects for each time chunk
        data = self.create_30_min_availabilities(
            start_time, end_time)
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data) 

        try:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) 
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        

    def create_30_min_availabilities(self, start_time, end_time):
        chunk_size = timedelta(minutes=30)
        # Create a list of Availability objects for each time chunk
        availabilities = []
        while start_time < end_time:
            availability = {
                "start_time": start_time,
                "end_time": start_time + chunk_size,
            }
            availabilities.append(availability)
            start_time += chunk_size
        return availabilities
