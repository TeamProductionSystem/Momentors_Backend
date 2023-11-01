from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from team_production_system.models import CustomUser


class UserProfilePatchTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(
          username="baby_yoda",
          email="grogu@mandalor.edu",
          password="badpassword"
        )

    def test_new_user_gets_random_photo_assigned(self):
        # Check that the user has a profile photo
        self.assertIsNotNone(self.user.profile_photo)

    def test_profile_photo_uploaded_first_time(self):
        # mock photo file
        photo = SimpleUploadedFile(
          "photo.jpg",
          b"this is a photo",
          content_type="image/jpeg"
        )
        # Make a PATCH request to update the user profile with the new photo
        url = reverse("my-profile")
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"profile_photo": photo})

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the profile photo was saved to the UserProfile object
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.profile_photo)

    def test_previous_file_deleted_when_new_photo_saved(self):
        # get name of existing profile photo file
        old_photo_name = self.user.profile_photo.name
        # Create a new profile photo file
        new_photo = SimpleUploadedFile(
          "new_photo.jpg",
          b"this is a new photo",
          content_type="image/jpeg"
        )

        # Make a PATCH request to update the user profile with the new photo
        url = reverse("my-profile")
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"profile_photo": new_photo})

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the new profile photo was saved
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.profile_photo.name, old_photo_name)

        # Check that the previous profile photo file was deleted from storage
        self.assertFalse(self.user.profile_photo.storage.exists(old_photo_name))
