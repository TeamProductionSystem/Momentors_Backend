from rest_framework import serializers
from team_production_system.models import Mentee


# Serializer for the mentee profile
class MenteeProfileSerializer(team_production_system.serializers.MenteeProfileSerializer):
    class Meta:
        model = Mentee
        fields = ('team_number',)
