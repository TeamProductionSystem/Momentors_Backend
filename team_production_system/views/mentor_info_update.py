from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from team_production_system.serializers import MentorProfileSerializer


# View to edit the logged in mentors about me and skills
class MentorInfoUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MentorProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        return self.request.user.mentor
