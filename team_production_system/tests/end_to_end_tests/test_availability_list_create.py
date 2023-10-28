from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ...models import Availability, CustomUser, Mentor
from ...serializers import AvailabilitySerializer


class AvailabilityListCreateTestCase(APITestCase):
    def setUp(self):
        # Create a Mentor object
        self.user = CustomUser.objects.create_user(
            username='mentor',
            email='mentor@example.com',
            password='password'
        )
        self.mentor = Mentor.objects.create(user=self.user)

        # Create two Availability objects associated with the Mentor
        self.availability1 = Availability.objects.create(
            mentor=self.mentor,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1)
        )
        self.availability2 = Availability.objects.create(
            mentor=self.mentor,
            start_time=timezone.now() + timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1, hours=1)
        )
        # Create a Client
        self.client = APIClient()

    def test_get_availability_list_without_authentication(self):
        """
        Test that a GET request to retrieve the list of Availabilities without
        authentication returns a status code of 401 UNAUTHORIZED.
        """
        # Send a GET request to retrieve the list of Availabilities
        url = reverse('availability')
        response = self.client.get(url, format='json')

        # Check that the response has a status code of 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_availability_list(self):
        """
        Test that a GET request to retrieve the list of Availabilities returns
        a status code of 200 OK and the correct serialized data.
        """

        # Authenticate as the Mentor
        self.client.force_authenticate(user=self.user)

        # Send a GET request to retrieve the list of Availabilities
        url = reverse('availability')
        response = self.client.get(url, format='json')

        # Check that the response has a status code of 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data matches the serialized Availability obj
        availabilities = Availability.objects.filter(
            mentor=self.mentor,
            end_time__gte=timezone.now()
        ).select_related('mentor__user')
        serializer = AvailabilitySerializer(availabilities, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_create_availability(self):
        """
        Test that a POST request to create a new Availability with valid data
        returns a status code of 201 CREATED.
        """

        # Authenticate as the Mentor
        self.client.force_authenticate(user=self.user)

        # Send a POST request to create a new Availability
        data = {
            'mentor': self.mentor.pk,
            'start_time': timezone.now() + timezone.timedelta(days=2),
            'end_time': timezone.now() + timezone.timedelta(days=2, hours=1)
        }
        url = reverse('availability')
        response = self.client.post(url, data, format='json')

        # Check that the response has a status code of 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the created Availability object has the correct attributes
        availability = Availability.objects.last()
        self.assertEqual(availability.start_time, data['start_time'])
        self.assertEqual(availability.end_time, data['end_time'])
        self.assertEqual(availability.mentor, self.mentor)

    def test_create_availability_with_duplicate_start_time(self):
        """
        Test that a POST request to create a new Availability with a start time
        that has already been used returns a status code of 400 BAD REQUEST
        and an error message.
        """
        # Authenticate as the Mentor
        self.client.force_authenticate(user=self.user)

        '''Send a POST request to create a new Availability with
        a start time that has already been used'''
        data = {
            'mentor': self.mentor.pk,
            'start_time': self.availability1.start_time,
            'end_time': timezone.now() + timezone.timedelta(hours=2)
        }
        url = reverse('availability')
        response = self.client.post(url, data, format='json')

        # Check that the response has a status code of 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the response data contains an error message
        self.assertEqual(response.data[0],
                         'Input overlaps with existing availability.')

    def test_create_availability_with_duplicate_start_and_end_times(self):
        """
        Test that a POST request to create a new Availability with a start time
        and end time that have already been used returns a status code of
        400 BAD REQUEST and an error message.
        """
        # Authenticate as the Mentor
        self.client.force_authenticate(user=self.user)

        # Send a POST request to create a new Availability with duplicate
        # start and end times
        data = {
            'mentor': self.mentor.pk,
            'start_time': self.availability1.start_time,
            'end_time': self.availability1.end_time
        }
        url = reverse('availability')
        response = self.client.post(url, data, format='json')

        # Check that the response has a status code of 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the response data contains an error message
        self.assertEqual(response.data[0],
                         'Input overlaps with existing availability.')

    def test_create_availability_with_end_time_before_start_time(self):
        """
        Test that a POST request to create a new Availability with a start time
        after the end time returns a status code of 400 BAD REQUEST.
        """
        # Authenticate as the Mentor
        self.client.force_authenticate(user=self.user)

        availability_data = {
            'start_time': '2022-01-01T14:00:00Z',
            'end_time': '2022-01-01T12:00:00Z',
            'mentor': self.mentor.pk
        }
        response = self.client.post('/availability/',
                                    availability_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['end_time'][0]),
                         'End time must be in the future.')
        self.assertEqual(Availability.objects.count(), 2)

    def test_create_availability_inside_existing_availability(self):
        """
        Test that a POST request to create a new Availability with a start time
        and end time that are inside an existing Availability returns a status
        code of 400 BAD REQUEST.
        """
        # Authenticate as the Mentor
        self.client.force_authenticate(user=self.user)

        availability_data = {
            'start_time': self.availability1.start_time +
            timezone.timedelta(minutes=15),
            'end_time': self.availability1.end_time -
            timezone.timedelta(minutes=15),
            'mentor': self.mentor.pk
        }
        response = self.client.post('/availability/',
                                    availability_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data[0]),
                         'Input overlaps with existing availability.')
        self.assertEqual(Availability.objects.count(), 2)
