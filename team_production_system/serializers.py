from rest_framework import serializers
from .models import Mentor, Mentee, SessionRequestForm, CustomUser, Availability, Session


# The serializer for the user information
class CustomUserSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField()

    class Meta:
        model = CustomUser
        fields = [
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile_photo',
            'is_mentor',
            'is_mentee',
            'is_active',
        ]

#     def update(self, instance, validated_data):
#         profile_photo = validated_data.get('profile_photo', None)
#         if profile_photo:
#             instance.profile_photo = profile_photo
#             instance.save()
#         return instance


# Serializer to show a list of all users flagged as a mentor
class MentorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentor
        fields = ('first_name', 'last_name', 'email',
                  'about_me', 'skill', 'mentor_photo')


# Serializer to show a list of all users flagged as a mentee
class MenteeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentee
        fields = ('first_name', 'last_name', 'email',
                  'about_me', 'team_number', 'mentor_photo')


# The serializer for the session request form
class SessionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionRequestForm
        fields = ('project', 'help_text', 'git_link', 'confirmed')


# The mentor avalablity serializer
class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ('pk', 'mentor', 'start_time', 'end_time')


# Serializer to show session information
class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('pk', 'mentor_availability', 'mentee',
                  'start_time', 'status', 'session_length', 'end_time')
