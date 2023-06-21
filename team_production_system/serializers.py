from rest_framework import serializers, fields
from .models import Mentor, Mentee, CustomUser
from .models import Availability, Session, NotificationSettings
from django.utils import timezone


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


# The mentor availability serializer
class AvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Availability
        fields = ('pk', 'mentor', 'start_time', 'end_time',)
        read_only_fields = ('mentor',)

    def create(self, validated_data):
        mentor = Mentor.objects.get(user=self.context['request'].user)
        start_time = self.data['start_time']
        end_time = self.data['end_time']
        overlapping_start = Availability.objects.filter(
            start_time__gte=start_time, 
            start_time__lte=start_time).count()
        overlapping_end = Availability.objects.filter(
            end_time__gte=end_time, 
            end_time__lte=end_time).count()
        availability_overlap = overlapping_start > 0 or overlapping_end > 0
        if availability_overlap == False:
            availability = Availability.objects.create(
                mentor=mentor, **validated_data)
            return availability
        else:
            raise serializers.ValidationError(
                "Input overlaps with existing availability.")


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
            availabilities = Availability.objects.filter(mentor=obj.pk,
                                                         end_time__gte=timezone.now())
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
    mentee_first_name = serializers.SlugField(source='mentee.user.first_name',
                                              read_only=True)
    mentee_last_name = serializers.SlugField(source='mentee.user.last_name',
                                             read_only=True)

    class Meta:
        model = Session
        fields = ('pk', 'mentor_first_name', 'mentor_last_name',
                  'mentor_availability', 'mentee', 'mentee_first_name', 'mentee_last_name', 'start_time', 'end_time', 'status', 'session_length',)
        read_only_fields = ('mentor', 'mentor_first_name', 'mentor_last_name',
                            'mentee', 'mentee_first_name', 'mentee_last_name')


# Serializer for notification settings
class NotificationSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationSettings
        fields = ('pk', 'user', 'session_requested', 'session_confirmed',
                  'session_canceled', 'fifteen_minute_alert', 'sixty_minute_alert',)
