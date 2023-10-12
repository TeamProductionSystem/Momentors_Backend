from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta, datetime
from django.utils.dateparse import parse_datetime
from team_production_system.models import (
    Mentor,
    Availability,
)


# V1 API #
# The mentor availability serializer
class AvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Availability
        fields = ['pk', 'mentor', 'start_time', 'end_time', 'status']
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


# V2 API #
# TODO: update to namespace v2 in future

class AvailabilityListSerializerV2(serializers.ListSerializer):
    child = 'AvailabilitySerializerV2'

    class Meta:
        model = Availability
        fields = ['pk', 'mentor', 'start_time', 'end_time', 'status']


    def create(self, validated_data):
        for data in validated_data:
            mentor = Mentor.objects.select_related('user').get(
                user=self.context['request'].user)
            start_time = data['start_time']
            end_time = data['end_time']

            availability_overlap = self.check_availability_overlap(
                mentor, start_time, end_time)
            start_time_valid = self.check_start_time(data)
            end_time_valid = self.check_end_time(end_time)

        if not availability_overlap or start_time_valid or end_time_valid:
            availabilities = []
            for availability in validated_data:
                instance = Availability(
                    mentor=mentor,
                    start_time=availability['start_time'],
                    end_time=availability['end_time'],
                    status='Open'
                )
                availabilities.append(instance)
            Availability.objects.bulk_create(availabilities)
            return availabilities

        raise serializers.ValidationError(
            "Input overlaps with existing availability.")

    # def update(self, instance, validated_data):
    #     # Map for id->instance
    #     availability_mapping = {availability.pk: availability for availability in instance}

    #     # Create a list of updated Availability objects
    #     updated_availabilities = []
    #     for availability_data in validated_data:

    #         pk = availability_data.get('pk', None)
    #         availability = availability_mapping.get(pk, None)
    #         if availability is not None:
    #             start_time = availability_data.get('start_time', availability.start_time)
    #             end_time = availability_data.get('end_time', availability.end_time)
    #             status = availability_data.get('status', availability.status)

    #             mentor = Mentor.objects.select_related('user').get(
    #                 user=self.context['request'].user)

    #             availability_overlap = self.check_availability_overlap(
    #                 mentor, start_time, end_time, availability.pk)

    #             if not availability_overlap:
    #                 start_time_valid = self.check_start_time(start_time)
    #                 end_time_valid = self.check_end_time(end_time)

    #                 if start_time_valid and end_time_valid:
    #                     availability.mentor = mentor
    #                     availability.start_time = start_time
    #                     availability.end_time = end_time
    #                     availability.status = status
    #                     availability.modified_at = datetime.now()
    #                     updated_availabilities.append(availability)
    #                 else:
    #                     raise serializers.ValidationError(
    #                         "Invalid start or end time.")
    #             else:
    #                 raise serializers.ValidationError(
    #                     "Input overlaps with existing availability.")

    #     # Use bulk_update to update all of the Availability objects in a single query
    #     Availability.objects.bulk_update(updated_availabilities, ['mentor', 'start_time', 'end_time', 'status', 'modified_at'])

    #     # Refresh the instance queryset to reflect the updated data
    #     instance = Availability.objects.filter(pk__in=[availability.pk for availability in updated_availabilities])

    #     return instance


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
    
    def check_start_time(self, data):
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

    def check_end_time(self, end_time):
        """
        Check that the end_time is in the future.
        """
        if end_time <= timezone.now():
            raise serializers.ValidationError(
                'End time must be in the future.'
            )
        return end_time


# The mentor availability serializer
class AvailabilitySerializerV2(serializers.ModelSerializer):

    class Meta:
        model = Availability
        fields = ['pk', 'mentor', 'start_time', 'end_time', 'status']
        read_only_fields = ('mentor', 'pk',)
        list_serializer_class = AvailabilityListSerializerV2
