from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from team_production_system.models import Mentee
from team_production_system.serializers import MenteeProfileSerializer

# View to allow mentees to create and view the about me/skills.


class MenteeInfoView(generics.ListCreateAPIView):
    serializer_class = MenteeProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Mentee.objects.filter(user=self.request.user)
