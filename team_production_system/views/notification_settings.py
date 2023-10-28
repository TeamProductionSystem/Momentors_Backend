from rest_framework import generics

from team_production_system.custom_permissions import (
    NotificationSettingsPermission
)
from team_production_system.models import NotificationSettings
from team_production_system.serializers import NotificationSettingsSerializer


class NotificationSettingsView(generics.RetrieveUpdateAPIView):
    queryset = NotificationSettings.objects.all()
    serializer_class = NotificationSettingsSerializer
    permission_classes = [NotificationSettingsPermission]
