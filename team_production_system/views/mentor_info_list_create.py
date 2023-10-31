from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from team_production_system.models import Mentor
from team_production_system.serializers import MentorProfileSerializer


# View to allow mentors to create and view the about me/skills.
class MentorInfoView(generics.ListCreateAPIView):
    serializer_class = MentorProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Mentor.objects.filter(user=self.request.user)
