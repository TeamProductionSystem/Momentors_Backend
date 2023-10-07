from django.test import TestCase
from ....models import Mentor, CustomUser


class MentorModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser',
                                              password='password123')

    def test_mentor_creation(self):
        mentor = Mentor.objects.create(
            user=self.user,
            about_me='This is a test about me.',
            team_number=5,
            skills=['HTML', 'CSS', 'Django']
        )

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

        self.assertEqual(str(mentor), 'testuser')

    def test_default_about_me(self):
        mentor = Mentor.objects.create(
            user=self.user,
            skills=['HTML']
        )

        self.assertEqual(mentor.about_me, '')

    def test_default_team_number(self):
        mentor = Mentor.objects.create(
            user=self.user,
            skills=['HTML']
        )

        self.assertEqual(mentor.team_number, 0)
