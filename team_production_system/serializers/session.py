from rest_framework import serializers
from team_production_system.models import Session


class SessionSerializer(serializers.ModelSerializer):
    mentor_first_name = serializers.SlugField(
        source='mentor.user.first_name',
        read_only=True,
    )
    mentor_last_name = serializers.SlugField(
        source='mentor.user.last_name',
        read_only=True,
    )
    mentee_first_name = serializers.SlugField(
        source='mentee.user.first_name',
        read_only=True,
    )
    mentee_last_name = serializers.SlugField(
        source='mentee.user.last_name',
        read_only=True,
    )

    class Meta:
        model = Session
        fields = (
            'pk',
            'mentor',
            'mentor_first_name',
            'mentor_last_name',
            'mentor_availability',
            'mentee',
            'mentee_first_name',
            'mentee_last_name',
            'start_time',
            'end_time',
            'status',
            'session_length',
        )
        read_only_fields = (
            'mentor',
            'mentor_first_name',
            'mentor_last_name',
            'mentee',
            'mentee_first_name',
            'mentee_last_name',
        )
