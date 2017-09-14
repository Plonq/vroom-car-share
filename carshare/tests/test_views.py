from django.test import TestCase, override_settings
from django.urls import reverse

# Tests do not work with whitenoise static file storage, so we use the default storage for tests
STATICFILES_STORAGE_FOR_TESTS = 'django.contrib.staticfiles.storage.StaticFilesStorage'


@override_settings(STATICFILES_STORAGE=STATICFILES_STORAGE_FOR_TESTS)
class IndexViewTests(TestCase):

    def test_homepage_returns_200(self):
        """
        Homepage correctly returns status code 200
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_contains_text_home(self):
        """
        Homepage correctly contains "Home"
        """
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Home')