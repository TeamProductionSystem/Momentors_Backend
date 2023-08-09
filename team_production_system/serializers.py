from rest_framework import serializers, fields
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes
from .models import Mentor, Mentee, CustomUser
from .models import Availability, Session, NotificationSettings


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
@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name='Example 1',
            value={
                'pk': 19,
                'mentor': 4,
                'start_time': '1999-12-31T14:30:00Z',
                'end_time': '1999-12-31T15:30:00Z',
            },
            response_only=True,
        ),
        OpenApiExample(
            name='Example 2',
            value={
                'pk': 20,
                'mentor': 5,
                'start_time': '1999-12-31T14:30:00Z',
                'end_time': '1999-12-31T15:30:00Z',
            },
            response_only=True,
        ),
        OpenApiExample(
            name='Example 3',
            value={
                'pk': 21,
                'mentor': 4,
                'start_time': '1999-12-31T15:30:00Z',
                'end_time': '1999-12-31T16:00:00Z',
            },
            response_only=True,
        ),
        OpenApiExample(
            name='Example 2',
            value={
                'pk': 22,
                'mentor': 7,
                'start_time': '1999-12-31T14:30:00Z',
                'end_time': '1999-12-31T15:30:00Z',
            },
            response_only=True,
        ),
    ]
)
class AvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Availability
        fields = ('pk', 'mentor', 'start_time', 'end_time',)
        read_only_fields = ('mentor', 'pk',)

    def create(self, validated_data):
        mentor = Mentor.objects.select_related('user').get(
            user=self.context['request'].user)
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']
        overlapping_start = Availability.objects.filter(
            mentor=mentor,
            start_time__lte=end_time,
            start_time__gte=start_time + timedelta(minutes=1)
            ).exists()
        overlapping_end = Availability.objects.filter(
            mentor=mentor,
            end_time__gte=start_time + timedelta(minutes=1),
            end_time__lte=end_time
            ).exists()
        availability_overlap = overlapping_start or overlapping_end
        if not availability_overlap:
            availability = Availability.objects.create(
                mentor=mentor, **validated_data)
            return availability
        raise serializers.ValidationError(
                "Input overlaps with existing availability.")

    def validate(self, data):
        """
        Check that the start_time is before the end_time.
        """
        start_time = data['start_time']
        end_time = data['end_time']
        if start_time >= end_time:
            raise serializers.ValidationError(
                'End time must be after start time.')
        return data

    def validate_end_time(self, value):
        """
        Check that the end_time is in the future.
        """
        if value <= timezone.now():
            raise serializers.ValidationError(
                'End time must be in the future.'
                )
        return value

    # TODO: Add validation for start times


# Serializer for the mentor profile
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
        fields = (
            'pk',
            'username',
            'first_name',
            'last_name',
            'profile_photo',
            'is_mentor', 'about_me',
            'skills',
            'availabilities',
        )

    @extend_schema_field(OpenApiTypes.STR)
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


# Serializer for the mentee profile
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
        fields = (
            'user',
            'pk',
            'username',
            'first_name',
            'last_name',
            'is_mentee',
            'mentee_profile',
        )


# Serializer to show session information
@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name='Example',
            value={
                'pk': 1,
                'mentor_first_name': 'Test',
                'mentor_last_name': 'Mentor',
                'mentor_availability': 1,
                'mentee': 3,
                'mentee_first_name': 'Test',
                'mentee_last_name': 'Mentee',
                'start_time': '2023-05-22T12:00:00Z',
                'end_time': '2023-05-22T12:30:00Z',
                'status': 'Confirmed',
                'session_length': 30,
            },
            response_only=True,
        ),
    ]
)
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


# Serializer for notification settings
class NotificationSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationSettings
        fields = (
            'pk',
            'user',
            'session_requested',
            'session_confirmed',
            'session_canceled',
            'fifteen_minute_alert',
            'sixty_minute_alert',
        )
