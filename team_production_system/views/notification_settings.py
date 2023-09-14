from rest_framework import generics
from team_production_system.custom_permissions import (
    NotificationSettingsPermission
)
from team_production_system.serializers import NotificationSettingsSerializer
from team_production_system.models import NotificationSettings


class NotificationSettingsView(generics.RetrieveUpdateAPIView):
    queryset = NotificationSettings.objects.all()
    serializer_class = NotificationSettingsSerializer
    permission_classes = [NotificationSettingsPermission]
