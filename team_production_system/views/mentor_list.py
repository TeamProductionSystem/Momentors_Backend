from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from team_production_system.models import CustomUser
from team_production_system.serializers import MentorListSerializer

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
