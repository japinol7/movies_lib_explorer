from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from catalog.models.director import Director


PHOTO_FILE_NAME = 'jpinol_young.jpg'


class UploadTestCase(TestCase):
    PASSWORD = 'test_asPg*f33'

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(f'testy', f'testy@example.com', self.PASSWORD)

    def test_photo_upload(self):
        director = Director.objects.create(first_name="Robert", last_name="California")
        director_url = reverse('director', args=(director.id,))
        upload_url = reverse('upload_director_photo', args=(director.id,))

        # Test upload button isn't there if not signed in
        response = self.client.get(director_url)
        self.assertEqual(200, response.status_code)
        self.assertNotIn('id="id_director_upload"', str(response.content))

        # Test login_required fires
        response = self.client.get(upload_url)
        self.assertEqual(302, response.status_code)
        self.assertIn('login', response.url)

        # Sign-in, check for button
        self.client.login(username=self.user, password=self.PASSWORD)
        response = self.client.get(director_url)
        self.assertEqual(200, response.status_code)
        self.assertIn('id="id_director_upload"', str(response.content))

        # Test image upload
        with open(f"tests/data/{PHOTO_FILE_NAME}", 'rb') as f:
            content = f.read()
            photo = SimpleUploadedFile(PHOTO_FILE_NAME, f.read(), 'image/jpeg')
            data = {
                'director_photo': photo,
                }
            response = self.client.post(upload_url, data)
            self.assertEqual(302, response.status_code)
            self.assertIn('director', response.url)

        # Re-fetch Director, should now have a file field
        director = Director.objects.get(id=director.id)
        self.assertEqual(f"1_{PHOTO_FILE_NAME}", director.picture.name)

        # Clean up
        path = Path(settings.MEDIA_ROOT) / f"1_{PHOTO_FILE_NAME}"
        path.unlink()
