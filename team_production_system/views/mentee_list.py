from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from team_production_system.models import CustomUser
from team_production_system.serializers import MenteeListSerializer


class MenteeList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            queryset = CustomUser.objects.filter(
                is_mentee=True).select_related("mentee")
        except Exception:
            return Response({"error": "Failed to retrieve mentee list."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not queryset.exists():
            return Response({"message": "No mentees found."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = MenteeListSerializer(queryset, many=True)
        response_data = serializer.data
        return Response(response_data)
