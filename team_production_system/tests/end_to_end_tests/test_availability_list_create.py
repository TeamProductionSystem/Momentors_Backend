from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from ...models import Availability, Mentor, CustomUser
from ...serializers import AvailabilitySerializer


class AvailabilityTestCase(APITestCase):
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

    # Test get request to retrieve all availabilities
    def test_get_availability_list(self):
        # Authenticate as the Mentor
        self.client.force_authenticate(user=self.user)

        # Send a GET request to retrieve the list of Availabilities
        url = reverse('availability')
        response = self.client.get(url, format='json')

        # Check that the response has a status code of 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data matches the serialized Availability objects
        availabilities = Availability.objects.filter(
            mentor=self.mentor,
            end_time__gte=timezone.now()
        ).select_related('mentor__user')
        serializer = AvailabilitySerializer(availabilities, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    # Test POST request to create an availability with valid data
    def test_create_availability(self):
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
