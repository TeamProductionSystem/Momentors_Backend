from datetime import datetime
from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone
from rest_framework import serializers
from ....serializers import AvailabilitySerializer, AvailabilitySerializerV2
from ....models import Mentor, CustomUser, Availability


class AvailabilitySerializerTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', password='testpass')
        self.mentor = Mentor.objects.create(user=self.user)
        self.availability_attributes = {
            'mentor': self.mentor,
            'start_time': datetime.now(
                timezone.utc) + timezone.timedelta(hours=4),
            'end_time': datetime.now(
                timezone.utc) + timezone.timedelta(hours=5),
        }
        self.serializer_data = {
            'mentor': self.mentor.pk,
            'start_time': self.availability_attributes['start_time'],
            'end_time': self.availability_attributes['end_time'],
        }
        self.availability = Availability.objects.create(
            **self.availability_attributes)
        self.request = HttpRequest()
        self.request.user = self.user
        self.serializer = AvailabilitySerializer(
            instance=self.availability,
            context={'request': self.request})

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_keys = ['pk', 'mentor', 'start_time', 'end_time']
        self.assertCountEqual(data.keys(), expected_keys)

    def test_mentor_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['mentor'], self.mentor.pk)

    def test_start_time_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['start_time'],
            self.serializer_data[
                'start_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        )

    def test_end_time_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['end_time'],
            self.serializer_data[
                'end_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        )

    def test_create(self):
        start_time = datetime.now(timezone.utc) + timezone.timedelta(hours=5)
        end_time = datetime.now(timezone.utc) + timezone.timedelta(hours=6)
        serializer_data = {
            'mentor': self.mentor.pk,
            'start_time': start_time,
            'end_time': end_time,
        }
        serializer = AvailabilitySerializer(
            data=serializer_data,
            context={'request': self.request}
            )
        self.assertTrue(serializer.is_valid())
        availability = serializer.save()
        self.assertEqual(availability.mentor, self.mentor)
        self.assertEqual(availability.start_time, start_time)
        self.assertEqual(availability.end_time, end_time)


# Test class for AvailabilitySerializerV2
class AvailabilitySerializerV2TestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', password='testpass')
        self.mentor = Mentor.objects.create(user=self.user)
        self.request = HttpRequest()
        self.request.user = self.user
        self.availability_attributes = {
            'mentor': self.mentor,
            'start_time': timezone.now() + timezone.timedelta(hours=3),
            'end_time': timezone.now() + timezone.timedelta(hours=4),
        }
        self.serializer_data = {
            'mentor': self.mentor.pk,
            'start_time': self.availability_attributes['start_time'],
            'end_time': self.availability_attributes['end_time'],
        }
        self.availability = Availability.objects.create(
            **self.availability_attributes)
        self.serializer = AvailabilitySerializerV2(
            instance=self.availability,
            context={'request': self.request})

    # Test that the serializer contains the expected fields
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(
            ['pk', 'mentor', 'start_time', 'end_time', 'status']))

    def test_create(self):
        pass

    # Test validate method
    def test_validate(self):
        serializer = AvailabilitySerializerV2(
            context={'request': self.request})
        start_time = datetime.now(
            timezone.utc) + timezone.timedelta(hours=1)
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
