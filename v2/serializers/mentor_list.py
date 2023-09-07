from rest_framework import serializers
from django.utils import timezone
from .availability import AvailabilitySerializer
from team_production_system.models import (
    CustomUser,
    Mentor,
    Availability,
    )

# Serializer to show a list of all users flagged as a mentor


class MentorListSerializer(serializers.ModelSerializer):
    about_me = serializers.SerializerMethodField('get_about_me')
    skills = serializers.SerializerMethodField('get_skills')
    availabilities = serializers.SerializerMethodField('get_availabilities')

    class Meta:
        model = CustomUser
        fields = ('pk', 'username', 'first_name',
                  'last_name', 'profile_photo', 'is_mentor', 'about_me',
                  'skills', 'availabilities')

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
