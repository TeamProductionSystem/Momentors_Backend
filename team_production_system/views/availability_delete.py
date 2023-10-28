from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from team_production_system.custom_permissions import IsOwnerOrAdmin
from team_production_system.models import Availability
from team_production_system.serializers import AvailabilitySerializer


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
