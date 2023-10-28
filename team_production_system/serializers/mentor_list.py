from django.utils import timezone
from rest_framework import serializers

from team_production_system.models import Availability, CustomUser, Mentor

from .availability import AvailabilitySerializer

# Serializer to show a list of all users flagged as a mentor


class MentorListSerializer(serializers.ModelSerializer):
    about_me = serializers.SerializerMethodField('get_about_me')
    skills = serializers.SerializerMethodField('get_skills')
    availabilities = serializers.SerializerMethodField('get_availabilities')
    team_number = serializers.SerializerMethodField('get_team_number')

    class Meta:
        model = CustomUser
        fields = (
            'pk',
            'username',
            'first_name',
            'last_name',
            'profile_photo',
            'is_mentor',
            'about_me',
            'skills',
            'availabilities',
            'team_number',
        )

    def get_about_me(self, obj):
        try:
            mentor = Mentor.objects.get(user=obj.pk)
            return mentor.about_me
        except Mentor.DoesNotExist:
            return None

    def get_skills(self, obj):
        try:
            mentor = Mentor.objects.get(user=obj.pk)
            return mentor.skills
        except Mentor.DoesNotExist:
            return None

    def get_availabilities(self, obj):
        try:
            availabilities = Availability.objects.filter(
                mentor=obj.pk, end_time__gte=timezone.now())
            serializer = AvailabilitySerializer(
                instance=availabilities, many=True)
            return serializer.data
        except Mentor.DoesNotExist:
            return None

    def get_team_number(self, obj):
        try:
            mentor = Mentor.objects.get(user=obj.pk)
            return mentor.team_number
        except Mentor.DoesNotExist:
            return None
