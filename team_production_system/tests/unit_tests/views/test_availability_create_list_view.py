from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from ....models import Availability, CustomUser, Mentor
from ....serializers import AvailabilitySerializer, AvailabilitySerializerV2


class AvailabilityListCreateViewTestCase(TestCase):
    def setUp(self):
        # Create a Mentor instance for the test
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@fake.com', password='testpass'
        )
        self.mentor = Mentor.objects.create(user=self.user)

        # Create an Availability instance for the test
        self.availability = Availability.objects.create(
            mentor=self.mentor,
            start_time=timezone.now() + timezone.timedelta(hours=1),
            end_time=timezone.now() + timezone.timedelta(hours=2),
        )
        self.url = reverse('availability')

    @patch('django.utils.timezone')
    def test_get_availability_list(self, mock_timezone):
        """
        Test that the get method returns a list of Availabilities
        belonging to the logged in mentor and with an end time
        in the future.
        """

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Set up the mock timezone to return a fixed datetime
        mock_timezone.now.return_value = timezone.datetime(
            2022, 1, 1, tzinfo=timezone.utc
        )

        # Make a GET request to the AvailabilityList view
        response = self.client.get('/availability/', format='json')
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the response data contains the expected Availability
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['start_time'],
            self.availability.start_time.isoformat().replace('+00:00', 'Z'),
        )

    def test_create_availability_v1(self):
        """
        Test that a POST request to create a new Availability returns a status
        code of 201 CREATED and the new Availability.
        """
        # Authenticate as the Mentor
        client = APIClient()
        client.force_authenticate(user=self.user)

        # Send a POST request to create a new Availability
        data = {
            'mentor': self.mentor.pk,
            'start_time': timezone.now() + timezone.timedelta(hours=3),
            'end_time': timezone.now() + timezone.timedelta(hours=4),
        }

        response = client.post(self.url, data, format='json')

        # Check that the response has a status code of 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the response data is the new Availability
        availability = Availability.objects.last()
        serializer = AvailabilitySerializer(availability)
        self.assertEqual(response.data['start_time'], serializer.data['start_time'])

    def test_create_availability_v1_with_invalid_data(self):
        """
        Test that a POST request to create a new Availability with invalid data
        returns a status code of 400 BAD REQUEST and an error message.
        """
        # Authenticate as the Mentor
        client = APIClient()
        client.force_authenticate(user=self.user)

        # Send a POST request to create a new Availability with invalid data
        data = {
            'mentor': self.mentor.pk,
            'start_time': timezone.now() + timezone.timedelta(hours=2),
            'end_time': timezone.now() + timezone.timedelta(hours=1),
        }

        response = client.post(self.url, data, format='json')

        # Check that the response has a status code of 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the response data contains an error message
        self.assertEqual(str(response.data[0]), 'End time must be after start time.')

    def test_create_availability_v2(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        start_time = timezone.now() + timedelta(hours=5)
        end_time = start_time + timedelta(hours=1)
        data = {
            'start_time': start_time,
            'end_time': end_time,
        }
        headers = {'HTTP_ACCEPT': 'application/json; version=v2'}
        response = self.client.post(self.url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Availability.objects.count(), 3)
        availability = Availability.objects.last()
        self.assertEqual(availability.start_time, end_time - timedelta(minutes=30))
        self.assertEqual(availability.end_time, end_time)
        self.assertEqual(availability.mentor, self.mentor)

    def test_create_availability_v2_with_overlap(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        start_time = timezone.now() + timedelta(hours=7)
        end_time = start_time + timedelta(hours=8)
        Availability.objects.create(
            mentor=self.mentor, start_time=start_time, end_time=end_time
        )
        data = {
            'start_time': start_time,
            'end_time': end_time,
        }
        headers = {'HTTP_ACCEPT': 'application/json; version=v2'}
        response = self.client.post(self.url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Availability.objects.count(), 2)

    def test_create_availability_v2_with_past_end_time(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        start_time = timezone.now() + timedelta(hours=1)
        end_time = timezone.now() - timedelta(hours=1)
        data = {
            'start_time': start_time,
            'end_time': end_time,
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Availability.objects.count(), 1)

    def test_create_availability_v2_with_time_not_divisible_by_30(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        start_time = timezone.now() + timedelta(hours=2)
        end_time = timezone.now() + timedelta(hours=3, minutes=15)
        data = {
            'start_time': start_time,
            'end_time': end_time,
        }
        headers = {'HTTP_ACCEPT': 'application/json; version=v2'}
        response = self.client.post(self.url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)
        availability_1 = Availability.objects.get(pk=response.data[0]['pk'])
        availability_2 = Availability.objects.get(pk=response.data[1]['pk'])
        self.assertEqual(availability_1.end_time, start_time + timedelta(minutes=30))
        self.assertNotEqual(availability_2.end_time, end_time)
        self.assertEqual(availability_1.mentor, self.mentor)

    def test_list_availabilities_v2(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        headers = {'HTTP_ACCEPT': 'application/json; version=v2'}
        response = self.client.get(self.url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        availabilities = Availability.objects.filter(mentor=self.mentor)
        serializer = AvailabilitySerializerV2(availabilities, many=True)
        self.assertEqual(response.data, serializer.data)
