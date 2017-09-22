from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

# Tests do not work with whitenoise static file storage, so we use the default storage for tests
STATICFILES_STORAGE_FOR_TESTS = 'django.contrib.staticfiles.storage.StaticFilesStorage'


@override_settings(STATICFILES_STORAGE=STATICFILES_STORAGE_FOR_TESTS)
class CarshareIndexViewTests(TestCase):

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


@override_settings(STATICFILES_STORAGE=STATICFILES_STORAGE_FOR_TESTS)
class CarshareContactUsViewTests(TestCase):

    def test_contact_us_form(self):
        """
        Contact Us form correctly sends email to staff
        """
        form = {
            'contact_name': 'Contact Name',
            'contact_email': 'contactemail@test.com',
            'message': 'This is the message.',
        }
        response = self.client.post(reverse('contact_us'), data=form)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'New Contact Us from Contact Name')
        self.assertEqual(mail.outbox[0].body, 'This is the message.')
        self.assertEqual(mail.outbox[0].from_email, 'admin@vroomcs.org')
        self.assertEqual(mail.outbox[0].reply_to, ['contactemail@test.com'])
        self.assertEqual(mail.outbox[0].to, ['admin@vroomcs.org'])