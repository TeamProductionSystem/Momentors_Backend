from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from team_production_system.models import Mentor, Availability
from team_production_system.serializers import AvailabilitySerializer


class AvailabilityViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('availability-list')
        self.mentor = Mentor.objects.create(name='John Doe', skills='Python')
        self.availability1 = Availability.objects.create(
            mentor=self.mentor,
            start_time='2022-01-01T00:00:00Z',
            end_time='2022-01-01T01:00:00Z'
        )
        self.availability2 = Availability.objects.create(
            mentor=self.mentor,
            start_time='2022-01-02T00:00:00Z',
            end_time='2022-01-02T01:00:00Z'
        )

    def test_create_availability(self):
        data = {
            'start_time': '2022-01-01T00:00:00Z',
            'end_time': '2022-01-01T01:00:00Z'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        availability = Availability.objects.get(id=response.data['id'])
        self.assertEqual(availability.start_time.isoformat(),
                         '2022-01-01T00:00:00+00:00')
        self.assertEqual(availability.end_time.isoformat(),
                         '2022-01-01T01:00:00+00:00')
        self.assertEqual(availability.mentor, self.mentor)

    def test_get_availability_list(self):
        self.client.force_authenticate(user=self.mentor.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        serializer = AvailabilitySerializer([self.availability1,
                                             self.availability2], many=True)
        self.assertEqual(response.data, serializer.data)
