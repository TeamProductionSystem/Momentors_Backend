from rest_framework import generics
from datetime import timedelta
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from team_production_system.serializers import SessionSerializer
from team_production_system.models import Session


# View to show mentor time slots a mentee can sign up for
class SessionSignUpListView(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter out completed sessions
        return Session.objects.exclude(status='Completed',
                                       start_time__lt=timezone.now() -
                                       timedelta(hours=24))
