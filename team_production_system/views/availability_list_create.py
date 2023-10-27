from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from team_production_system.serializers import (
    AvailabilitySerializer,
    AvailabilitySerializerV2
)
from team_production_system.models import Mentor, Availability
from team_production_system.helpers import create_30_min_availabilities


# Create and view all availabilities
class AvailabilityListCreateView(generics.ListCreateAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        response = super().handle_exception(exc)

        if isinstance(response.data, dict) and 'non_field_errors' in response.data:
            response.data = response.data['non_field_errors']

        return response

    def get_queryset(self):
        if self.request.version == 'v2':
            # Get the Mentor instance for the logged in user
            mentor = Mentor.objects.select_related('user').get(
                user=self.request.user)
            return Availability.objects.filter(
                mentor=mentor,
                end_time__gte=timezone.now()
            ).select_related('mentor__user').order_by('start_time')
        else:
            # Get the Mentor instance for the logged in user
            mentor = Mentor.objects.get(user=self.request.user)
            # Exclude any availability that has an end time in the past
            # and filter availabilities belonging to the logged in mentor
            return Availability.objects.filter(
                mentor=mentor, end_time__gte=timezone.now()
            ).select_related('mentor__user')

    def create(self, request, *args, **kwargs):
        if request.version == 'v2':
            # Validate data before creating 30 min availabilities
            request.data.update(mentor=request.user.mentor)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Create 30 min availabilities
            availabilities = create_30_min_availabilities(
                request.data['start_time'],
                request.data['end_time'],
                request.user.mentor
            )
            # Serialize and save 30 min availabilities
            serializer = self.get_serializer(data=availabilities, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return AvailabilitySerializerV2
        else:
            return AvailabilitySerializer
