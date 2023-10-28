from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from team_production_system.serializers import MenteeProfileSerializer


# View to edit the logged in mentees team number
class MenteeInfoUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenteeProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        return self.request.user.mentee
