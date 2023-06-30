from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from catalog.models.director import Director


PHOTO_FILE_NAME = 'jpinol_young.jpg'


class UploadDirectorPhotoTestCase(TestCase):
    PASSWORD = 'test_asPg*f33'

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(f'testy', f'testy@example.com', self.PASSWORD)
        self.director = Director.objects.create(first_name="Robert", last_name="California")
        self.director_url = reverse('catalog:director', args=(self.director.id,))
        self.upload_url = reverse('catalog:upload_director_photo', args=(self.director.id,))

    def test_photo_upload_redirection_to_login_if_not_signed_in(self):
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_photo_upload_not_there_if_user_is_not_staff(self):
        self.client.login(username=self.user, password=self.PASSWORD)
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('id="id_director_upload"', str(response.content))

    def test_photo_upload_possible_if_user_is_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.user, password=self.PASSWORD)
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id="id_director_photo"', str(response.content))

    def test_image_upload(self):
        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.user, password=self.PASSWORD)
        with open(f"tests/data/{PHOTO_FILE_NAME}", 'rb') as f:
            photo = SimpleUploadedFile(PHOTO_FILE_NAME, f.read(), 'image/jpeg')
            data = {
                'director_photo': photo,
                }
            response = self.client.post(self.upload_url, data)
            self.assertEqual(response.status_code, 302)
            self.assertIn('director', response.url)

        # Re-fetch Director, should now have a file field
        director = Director.objects.get(id=self.director.id)
        self.assertEqual(director.picture.name, f"1_director_{PHOTO_FILE_NAME}")

        # Clean up
        path = Path(settings.MEDIA_ROOT) / f"1_director_{PHOTO_FILE_NAME}"
        path.unlink()
