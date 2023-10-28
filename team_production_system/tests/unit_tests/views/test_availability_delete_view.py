from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ....models import Availability, CustomUser, Mentor


class AvailabilityDeleteViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser', password='testpass'
        )
        self.mentor = Mentor.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_object(self):
        # Create an Availability instance for the logged-in user
        availability = Availability.objects.create(
            mentor=self.mentor,
            start_time='2022-01-01T00:00:00Z',
            end_time='2022-01-01T01:00:00Z',
        )

        # Test that get_object returns the correct Availability instance
        url = reverse('availability-delete', args=[availability.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Test that get_object raises Http404 for non-existent Availability
        url = reverse('availability-delete', args=[availability.id + 1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
