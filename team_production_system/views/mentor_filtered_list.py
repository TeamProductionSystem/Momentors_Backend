from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from team_production_system.models import Mentor
from team_production_system.serializers import MentorProfileSerializer


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
