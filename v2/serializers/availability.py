from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from team_production_system.models import (
    Mentor,
    Availability,
)


# The mentor availability serializer
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
