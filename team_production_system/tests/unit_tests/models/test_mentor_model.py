from django.test import TestCase

from ....models import CustomUser, Mentor


class MentorModelTest(TestCase):

    def setUp(self):
        # Assuming CustomUser has a username and password
        self.user = CustomUser.objects.create(username='testuser',
                                              password='password123')

    def test_mentor_creation(self):
        mentor = Mentor.objects.create(
            user=self.user,
            about_me='This is a test about me.',
            team_number=5,
            skills=['HTML', 'CSS', 'Django']
        )

        # Assert that the mentor object was saved and has the correct
        # attributes
        self.assertEqual(mentor.about_me, 'This is a test about me.')
        self.assertEqual(mentor.team_number, 5)
        self.assertListEqual(list(mentor.skills), ['HTML', 'CSS', 'Django'])

    def test_str_representation(self):
        mentor = Mentor.objects.create(
            user=self.user,
            about_me='This is a test about me.',
            team_number=5,
            skills=['HTML']
        )

        # Assert that the __str__ method returns the correct representation
        self.assertEqual(str(mentor), 'testuser')

    def test_default_about_me(self):
        # Create a Mentor object without specifying an 'about_me'
        mentor = Mentor.objects.create(
            user=self.user,
            skills=['HTML']
        )

        # Assert that the default value for 'about_me' is set
        self.assertEqual(mentor.about_me, '')

    def test_default_team_number(self):
        # Create a Mentor object without specifying a 'team_number'
        mentor = Mentor.objects.create(
            user=self.user,
            skills=['HTML']
        )

        # Assert that the default value for 'team_number' is set
        self.assertEqual(mentor.team_number, 0)
