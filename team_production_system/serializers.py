from rest_framework import serializers, fields
from .models import Mentor, Mentee, CustomUser
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


# The mentor availability serializerx
class AvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Availability
        fields = ('pk', 'mentor', 'start_time', 'end_time',)
        read_only_fields = ('mentor',)

    def create(self, validated_data):
        mentor = Mentor.objects.get(user=self.context['request'].user)
        availability = Availability.objects.create(
            mentor=mentor, **validated_data)
        return availability


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
            availabilities = Availability.objects.filter(mentor=obj.pk)
            serializer = AvailabilitySerializer(
                instance=availabilities, many=True)
            return serializer.data
        except Mentor.DoesNotExist:
            return None


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


# Serializer to show session information
class SessionSerializer(serializers.ModelSerializer):
    mentor_first_name = serializers.SlugField(source='mentor.user.first_name',
                                              read_only=True)
    mentor_last_name = serializers.SlugField(source='mentor.user.last_name',
                                             read_only=True)

    class Meta:
        model = Session
        fields = ('pk', 'mentor_first_name', 'mentor_last_name',
                  'mentor_availability', 'mentee', 'start_time',
                  'end_time', 'status', 'session_length',)
        read_only_fields = ('mentor', 'mentor_first_name',
                            'mentor_last_name',)
