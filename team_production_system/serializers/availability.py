from django.utils import timezone
from team_production_system.models import (
    Mentor,
    Availability,
)
from team_production_system.helpers import (
    is_overlapping_availabilities,
    is_valid_start_time,
    is_valid_end_time
)
from rest_framework import serializers


# V_1 API #
# The mentor availability serializer
class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = (
            'pk',
            'mentor',
            'start_time',
            'end_time',
        )
        read_only_fields = (
            'mentor',
            'pk',
        )

    def create(self, validated_data):
        mentor = Mentor.objects.select_related('user').get(
            user=self.context['request'].user
        )
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']
        # Check if start time is between a start time and end time of
        # an existing availability
        overlapping_condition1 = Availability.objects.filter(
            mentor=mentor,
            start_time__lt=start_time,
            end_time__gt=start_time,
        ).exists()
        # Check if end time is between a start time and end time of
        # an existing availability
        overlapping_condition2 = Availability.objects.filter(
            mentor=mentor, start_time__lt=end_time, end_time__gt=end_time
        ).exists()
        # Check if start time is between the new start_time and new end_time
        overlapping_condition3 = Availability.objects.filter(
            mentor=mentor, start_time__gte=start_time, start_time__lt=end_time
        ).exists()
        # Check if end time is between the new start_time and new end_time
        overlapping_condition4 = Availability.objects.filter(
            mentor=mentor, end_time__gt=start_time, end_time__lte=end_time
        ).exists()

        availability_overlap = (
            overlapping_condition1
            or overlapping_condition2
            or overlapping_condition3
            or overlapping_condition4
        )
        if not availability_overlap:
            availability = Availability.objects.create(mentor=mentor, **validated_data)
            return availability

        raise serializers.ValidationError("Input overlaps with existing availability.")

    def validate(self, data):
        """
        Check that the start_time is before the end_time.
        """
        start_time = data['start_time']
        end_time = data['end_time']
        if start_time >= end_time:
            raise serializers.ValidationError('End time must be after start time.')

        return data

    def validate_end_time(self, value):
        """
        Check that the end_time is in the future.
        """
        if value <= timezone.now():
            raise serializers.ValidationError('End time must be in the future.')

        return value


# V2 API #
# The mentor availability serializer
class AvailabilitySerializerV2(serializers.ModelSerializer):

    class Meta:
        model = Availability
        fields = [
            'pk',
            'mentor',
            'start_time',
            'end_time',
            'status'
        ]
        read_only_fields = ('pk',)

    def validate(self, data):
        mentor = Mentor.objects.select_related('user').get(
            user=self.context['request'].user)
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if not is_valid_start_time(start_time):
            raise serializers.ValidationError(
                'Start time must be in the future.')

        if not is_valid_end_time(start_time, end_time):
            raise serializers.ValidationError(
                'End time must be after start time.')

        if is_overlapping_availabilities(mentor, data):
            raise serializers.ValidationError(
                'Availability overlaps with existing availability.')

        return data
