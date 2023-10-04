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
            mentor=mentor,
            start_time__lt=end_time,
            end_time__gt=end_time
        ).exists()
        # Check if start time is between the new start_time and new end_time
        overlapping_condition3 = Availability.objects.filter(
            mentor=mentor,
            start_time__gte=start_time,
            start_time__lt=end_time
        ).exists()
        # Check if end time is between the new start_time and new end_time
        overlapping_condition4 = Availability.objects.filter(
            mentor=mentor,
            end_time__gt=start_time,
            end_time__lte=end_time
        ).exists()

        availability_overlap = (
            overlapping_condition1
            or overlapping_condition2
            or overlapping_condition3
            or overlapping_condition4)
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
    

class AvailabilityV2Serializer(serializers.ModelSerializer):

    class Meta:
        model = Availability
        fields = ('pk', 'mentor', 'start_time', 'end_time', 'status')
        read_only_fields = ('mentor', 'pk',)

    def create(self, validated_data):
        mentor = Mentor.objects.select_related('user').get(
            user=self.context['request'].user)
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']

        availability_overlap = self.check_availability_overlap(
            mentor, start_time, end_time)

        if not availability_overlap:

            availabilities = self.create_30_min_availabilities(
                start_time, end_time, mentor)

            Availability.objects.bulk_create(availabilities)

            return validated_data

        raise serializers.ValidationError(
            "Input overlaps with existing availability.")

    def check_availability_overlap(self, mentor, start_time, end_time):
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
            mentor=mentor,
            start_time__lt=end_time,
            end_time__gt=end_time
        ).exists()
        # Check if start time is between the new start_time and new end_time
        overlapping_condition3 = Availability.objects.filter(
            mentor=mentor,
            start_time__gte=start_time,
            start_time__lt=end_time
        ).exists()
        # Check if end time is between the new start_time and new end_time
        overlapping_condition4 = Availability.objects.filter(
            mentor=mentor,
            end_time__gt=start_time,
            end_time__lte=end_time
        ).exists()

        availability_overlap = (
            overlapping_condition1
            or overlapping_condition2
            or overlapping_condition3
            or overlapping_condition4)
        return availability_overlap

    def create_30_min_availabilities(self, start_time, end_time, mentor):
        chunk_size = timedelta(minutes=30)

        # Create a list of Availability objects for each time chunk
        availabilities = []
        while start_time < end_time:
            availability = Availability(
                mentor=mentor,
                start_time=start_time,
                end_time=start_time + chunk_size,
            )
            availabilities.append(availability)
            start_time += chunk_size
        return availabilities

    def validate(self, data):
        """
        Check that the start_time is before the end_time and in future.
        """
        start_time = data['start_time']
        end_time = data['end_time']
        if start_time >= end_time:
            raise serializers.ValidationError(
                'End time must be after start time.')
        if start_time <= timezone.now():
            raise serializers.ValidationError(
                'Start time must be in the future.'
            )
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
