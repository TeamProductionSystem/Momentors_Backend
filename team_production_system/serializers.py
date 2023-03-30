from rest_framework import serializers
from .models import Mentor, Mentee, SessionRequestForm, CustomUser
from .models import Availability, Session


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


# The mentor availability serializer
class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ('pk', 'mentor', 'start_time', 'end_time')


class MentorProfileSerializer(serializers.ModelSerializer):
    availabilities = AvailabilitySerializer(many=True, read_only=True, source='mentor_availability')

    class Meta:
        model = Mentor
        fields = ('pk', 'about_me', 'skills', 'availabilities')
        read_only_fields = ('pk',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


# Serializer to show a list of all users flagged as a mentor
class MentorListSerializer(serializers.ModelSerializer):
    about_me = serializers.SerializerMethodField('get_about_me')
    skills = serializers.SerializerMethodField('get_skills')
    availabilities = serializers.SerializerMethodField('get_availabilities')

    class Meta:
        model = CustomUser
        fields = ('pk', 'username', 'first_name',
                  'last_name', 'profile_photo', 'is_mentor', 'about_me', 'skills', 'availabilities')

    def get_about_me(self, obj):
        mentor = Mentor.objects.get(user=obj.pk)
        return mentor.about_me

    def get_skills(self, obj):
        mentor = Mentor.objects.get(user=obj.pk)
        return mentor.skills

    def get_availabilities(self, obj):
        availabilities = Availability.objects.filter(mentor=obj.pk)
        serializer = AvailabilitySerializer(instance=availabilities, many=True)
        return serializer.data


class MenteeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentee
        fields = ('team_number',)


# Serializer to show a list of all users flagged as a mentee
class MenteeListSerializer(serializers.ModelSerializer):
    mentee_profile = MenteeProfileSerializer(read_only=True, source='mentee')
    user = CustomUserSerializer(read_only=True, source='customuser')

    class Meta:
        model = CustomUser
        fields = ('user', 'pk', 'username', 'first_name',
                  'last_name', 'is_mentee', 'mentee_profile')


# The serializer for the session request form
class SessionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionRequestForm
        fields = ('project', 'help_text', 'git_link', 'confirmed')


# Serializer to show session information
class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('pk', 'mentor_availability', 'mentee',
                  'start_time', 'status', 'session_length', 'end_time')
