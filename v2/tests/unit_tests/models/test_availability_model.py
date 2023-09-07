from django.test import TestCase
from datetime import datetime, timedelta, timezone
from ....models import Availability, Availability2, Mentor, CustomUser


class AvailabilityTestCase(TestCase):
    def setUp(self):
        # Create a User and Mentor object
        self.user = CustomUser.objects.create_user(
            username='mentor',
            email='mentor@example.com',
            password='password'
        )
        self.mentor = Mentor.objects.create(user=self.user)

    def test_create_availability2(self):
        # Set start and end times
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=1)

        # Create an Availability object
        availability = Availability2(
            mentor=self.mentor,
            start_time=start_time,
            end_time=end_time)

        # Save an Availability object associated with the Mentor
        availability.save()
        
        # Retrieve the saved Availability object
        first_saved_availability = Availability2.objects.first()
        second_saved_availability = Availability2.objects.last()
        count_availability = Availability2.objects.count()

        # Check that the object was saved correctly
        self.assertEqual(count_availability, 2)
        self.assertEqual(first_saved_availability.start_time, start_time)
        self.assertEqual(first_saved_availability.end_time, end_time - timedelta(minutes=30))
        self.assertEqual(first_saved_availability.mentor, self.mentor)
        self.assertEqual(str(first_saved_availability), f"{self.mentor} is available from {start_time} to {start_time + timedelta(minutes=30)}.")
        self.assertEqual(second_saved_availability.start_time, start_time + timedelta(minutes=30))
        self.assertEqual(second_saved_availability.end_time, start_time + timedelta(minutes=60))
        self.assertEqual(str(second_saved_availability), f"{self.mentor} is available from {start_time + timedelta(minutes=30)} to {start_time + timedelta(minutes=60)}.")

