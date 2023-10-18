from django.test import TestCase
from django.utils import timezone
from rest_framework import serializers
from django.http import HttpRequest
from ....serializers import AvailabilitySerializerV2
from ....models import Mentor, CustomUser


class AvailabilitySerializerV2TestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', password='testpass')
        self.mentor = Mentor.objects.create(user=self.user)
        self.request = HttpRequest()
        self.request.user = self.user

    def test_validate(self):
        serializer = AvailabilitySerializerV2(context={'request': self.request})
        start_time = timezone.now() + timezone.timedelta(hours=1)
        end_time = timezone.now() + timezone.timedelta(hours=2)
        data = {
            'start_time': start_time,
            'end_time': end_time
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
