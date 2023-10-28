# flake8: noqa

import unittest
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ..models import Availability, CustomUser, Mentor


@unittest.skip("Test file is not ready yet")
class AvailabilityTestCase(TestCase):
    def setUp(self):
        # Set up a mentor and an availability for testing
        self.mentor_user = CustomUser.objects.create_user(
            username='mentor_user',
            email='mentor_user@example.com',
            password='password'
        )
        self.mentor = Mentor.objects.create(
            user=self.mentor_user,
            about_me='I am a mentor',
            skills=['Python']
        )
        self.availability = Availability.objects.create(
            mentor=self.mentor,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1)
        )

    def test_is_available(self):
        # Test that an availability in the future is available
        self.assertTrue(self.availability.is_available())

        # Test that an availability in the past is not available
        self.availability.end_time = timezone.now() - timedelta(hours=1)
        self.assertFalse(self.availability.is_available())

    def test_get_next_seven_days_availability(self):
        # Test that the method returns the correct number of days
        availabilities = self.availability.get_next_seven_days_availability()
        self.assertEqual(len(availabilities), 8)

        # Test that the method returns the correct availability slots
        slot_start_time = timezone.now() + timedelta(days=2)
        slot_end_time = slot_start_time + timedelta(hours=1)
        availability = Availability.objects.create(
            mentor=self.mentor,
            start_time=slot_start_time,
            end_time=slot_end_time
        )
        availabilities = self.availability.get_next_seven_days_availability()
        self.assertEqual(len(availabilities[2][1]), 1)
        self.assertEqual(availabilities[2][1][0], availability)

    def test_is_slot_available(self):
        # Test that a slot is available when there are no other sessions scheduled
        start_time = timezone.now() + timedelta(hours=2)
        end_time = start_time + timedelta(hours=1)
        self.assertTrue(self.availability.is_slot_available(start_time, end_time))

        # Test that a slot is not available when there is another session scheduled during the same time
        Session.objects.create(
            mentor_availability=self.availability,
            mentee=self.mentee,
            start_time=start_time,
            session_length=60
        )
        self.assertFalse(self.availability.is_slot_available(start_time, end_time))
