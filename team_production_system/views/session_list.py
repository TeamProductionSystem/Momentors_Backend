from django.db.models import Q
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from team_production_system.models import Session
from team_production_system.serializers import SessionSerializer


class SessionView(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get sessions for the logged in user
        # Exclude sessions that have already ended and
        # order by sessions that are coming up next first.
        return Session.objects.filter(Q(mentor__user=self.request.user) |
                                      Q(mentee__user=self.request.user),
                                      start_time__gt=timezone.now()
                                      ).order_by('start_time')
