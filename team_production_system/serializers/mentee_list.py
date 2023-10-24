from rest_framework import serializers
from team_production_system.models import CustomUser
from .mentee_profile import MenteeProfileSerializer
from .custom_user import CustomUserSerializer


class MenteeListSerializer(serializers.ModelSerializer):
    mentee_profile = MenteeProfileSerializer(read_only=True, source='mentee')
    user = CustomUserSerializer(read_only=True, source='customuser')

    class Meta:
        model = CustomUser
        fields = (
            'user',
            'pk', 'username',
            'first_name',
            'last_name',
            'is_mentee',
            'mentee_profile'
        )
