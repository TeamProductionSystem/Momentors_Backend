from rest_framework import fields, serializers

from team_production_system.models import Mentor

from .availability import AvailabilitySerializer


class MentorProfileSerializer(serializers.ModelSerializer):
    availabilities = AvailabilitySerializer(
        many=True, read_only=True, source='mentor_availability')
    skills = fields.MultipleChoiceField(choices=Mentor.SKILLS_CHOICES)
    team_number = serializers.IntegerField(required=False)

    class Meta:
        model = Mentor
        fields = ('pk', 'about_me', 'skills', 'availabilities', 'team_number')
        read_only_fields = ('pk',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
