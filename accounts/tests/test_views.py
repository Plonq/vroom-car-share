from django.test import TestCase, override_settings
from django.shortcuts import reverse


# Tests do not work with whitenoise static file storage, so we use the default storage for tests
STATICFILES_STORAGE_FOR_TESTS = 'django.contrib.staticfiles.storage.StaticFilesStorage'


@override_settings(STATICFILES_STORAGE=STATICFILES_STORAGE_FOR_TESTS)
class AccountsPageTextViewTests(TestCase):
    def test_register_page(self):
        """
        Register page contains expected text
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")

    def test_login_page(self):
        """
        Login page contains expected text
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")