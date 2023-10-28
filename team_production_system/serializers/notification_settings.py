from rest_framework import serializers

from team_production_system.models import NotificationSettings


class NotificationSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationSettings
        fields = (
            'pk',
            'user',
            'session_requested',
            'session_confirmed',
            'session_canceled',
            'fifteen_minute_alert',
            'sixty_minute_alert',
        )
