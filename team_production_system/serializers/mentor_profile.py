from rest_framework import serializers, fields
from .availability import AvailabilitySerializer
from team_production_system.models import Mentor


class MentorProfileSerializer(serializers.ModelSerializer):
    availabilities = AvailabilitySerializer(
        many=True, read_only=True, source='mentor_availability')
    skills = fields.MultipleChoiceField(choices=Mentor.SKILLS_CHOICES)

    class Meta:
        model = Mentor
        fields = ('pk', 'about_me', 'skills', 'availabilities')
        read_only_fields = ('pk',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
