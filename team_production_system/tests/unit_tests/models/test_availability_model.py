from datetime import datetime, timedelta, timezone

from django.test import TestCase

from ....models import Availability, CustomUser, Mentor


class AvailabilityTestCase(TestCase):
    def setUp(self):
        # Create a User and Mentor object
        self.user = CustomUser.objects.create_user(
            username='mentor',
            email='mentor@example.com',
            password='password'
        )
        self.mentor = Mentor.objects.create(user=self.user)

    def test_create_availability(self):
        # Set start and end times
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=1)

        # Create an Availability object
        availability = Availability(
            mentor=self.mentor,
            start_time=start_time,
            end_time=end_time)

        # Save an Availability object associated with the Mentor
        availability.save()

        # Retrieve the saved Availability object
        saved_availability = Availability.objects.first()

        # Check that the object was saved correctly
        self.assertEqual(saved_availability.start_time, start_time)
        self.assertEqual(saved_availability.end_time, end_time)
        self.assertEqual(saved_availability.mentor, self.mentor)
        self.assertEqual(str(saved_availability),
                         f"{self.mentor} is available from "
                         f"{start_time} to {end_time}.")
