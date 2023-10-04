from django.test import TestCase
from django.utils import timezone
from rest_framework import serializers
from ....serializers import AvailabilitySerializerV2


class AvailabilitySerializerV2TestCase(TestCase):
    def test_validate(self):
        serializer = AvailabilitySerializerV2()
        start_time = timezone.now() + timezone.timedelta(hours=1)
        end_time = timezone.now() + timezone.timedelta(hours=2)
        data = {
            'start_time': start_time,
            'end_time': end_time,
        }
        # Test valid input data
        validated_data = serializer.validate(data)
        self.assertEqual(validated_data, data)

        # Test invalid start_time
        start_time = timezone.now() - timezone.timedelta(hours=1)
        end_time = timezone.now() + timezone.timedelta(hours=2)
        data = {
            'start_time': start_time,
            'end_time': end_time,
        }
        with self.assertRaises(serializers.ValidationError) as context:
            serializer.validate(data)
        self.assertEqual(
            str(context.exception.detail[0]),
            'Start time must be in the future.'
        )

        # Test invalid end_time
        start_time = timezone.now() + timezone.timedelta(hours=2)
        end_time = timezone.now() + timezone.timedelta(hours=1)
        data = {
            'start_time': start_time,
            'end_time': end_time,
        }
        with self.assertRaises(serializers.ValidationError) as context:
            serializer.validate(data)
        self.assertEqual(
            str(context.exception.detail[0]),
            'End time must be after start time.'
        )
