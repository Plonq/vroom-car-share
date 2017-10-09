from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

import datetime as dt

from ..models import Booking, User, Vehicle, Pod, VehicleType


# Tests do not work with whitenoise static file storage, so we use the default storage for tests
STATICFILES_STORAGE_FOR_TESTS = 'django.contrib.staticfiles.storage.StaticFilesStorage'


@override_settings(STATICFILES_STORAGE=STATICFILES_STORAGE_FOR_TESTS)
class CarshareIndexViewTests(TestCase):

    def test_homepage_returns_200(self):
        """
        Homepage correctly returns status code 200
        """
        response = self.client.get(reverse('carshare:index'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_contains_text_home(self):
        """
        Homepage correctly contains "Home"
        """
        response = self.client.get(reverse('carshare:index'))
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
        response = self.client.post(reverse('carshare:contact_us'), data=form)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'New Contact Us from Contact Name')
        self.assertEqual(mail.outbox[0].body, 'This is the message.')
        self.assertEqual(mail.outbox[0].from_email, 'admin@vroomcs.org')
        self.assertEqual(mail.outbox[0].reply_to, ['contactemail@test.com'])
        self.assertEqual(mail.outbox[0].to, ['admin@vroomcs.org'])


@override_settings(STATICFILES_STORAGE=STATICFILES_STORAGE_FOR_TESTS)
class CarshareBookingViewTests(TestCase):
    def setUp(self):
        # Create user to log in as
        User.objects.create_user(email='user@test.com', password='bigbadtestuser', first_name='Test', last_name='User', date_of_birth=dt.date(1980, 1, 1))

        # Set up some sample data, including a few bookings
        vt = VehicleType.objects.create(description='Premium', hourly_rate=12.50, daily_rate=80.00)
        p1 = Pod.objects.create(latitude='-39.34523453', longitude='139.53524344', description='Pod 1')
        p2 = Pod.objects.create(latitude='-38.34523453', longitude='138.53524344', description='Pod 2')
        self.v1 = Vehicle.objects.create(pod=p1, type=vt, name='Vehicle1', make='Toyota', model='Yaris', year=2012,
                                    registration='AAA222')
        self.v2 = Vehicle.objects.create(pod=p2, type=vt, name='Vehicle2', make='Toyota', model='Yaris', year=2011,
                                    registration='AAA223')
        u1 = User.objects.create(email='test1@test.com', first_name='John', last_name='Doe', date_of_birth='1980-01-01')
        u2 = User.objects.create(email='test2@test.com', first_name='Jane', last_name='Doly', date_of_birth='1988-01-01')
        # 12 AM - 1 AM
        self.b1 = Booking.objects.create(user=u1, vehicle=self.v1,
                               schedule_start=timezone.make_aware(dt.datetime(year=2999, month=1, day=1, hour=0)),
                               schedule_end=timezone.make_aware(dt.datetime(year=2999, month=1, day=1, hour=1)))
        # 3 AM - 6 AM
        self.b2 = Booking.objects.create(user=u1, vehicle=self.v1,
                               schedule_start=timezone.make_aware(dt.datetime(year=2999, month=1, day=1, hour=3)),
                               schedule_end=timezone.make_aware(dt.datetime(year=2999, month=1, day=1, hour=6)))

    def test_valid_booking(self):
        """
        Booking for a time period that is not already booked by the user or the vehicle is successfully created
        """
        form = {
            'booking_start_date': '01/01/3000',
            'booking_start_time': '00:00',
            'booking_end_date': '01/01/3000',
            'booking_end_time': '01:00',
        }
        self.client.login(email='user@test.com', password='bigbadtestuser')
        get_response = self.client.get(reverse('carshare:booking_create', kwargs={'vehicle_id': self.v1.id}))
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(reverse('carshare:booking_create', kwargs={'vehicle_id': self.v1.id}), data=form)
        booking_id = User.objects.get(email='user@test.com').booking_set.first().id
        self.assertRedirects(post_response, reverse('carshare:booking_detail', kwargs={'booking_id': booking_id}))

    def test_booking_for_time_period_already_booked(self):
        """
        Booking for a time period that overlaps with an existing booking for the same vehicle returns an error message
        """
        form = {
            'booking_start_date': '01/01/2999',
            'booking_start_time': '00:00',
            'booking_end_date': '01/01/2999',
            'booking_end_time': '01:00',
        }
        self.client.login(email='user@test.com', password='bigbadtestuser')
        get_response = self.client.get(reverse('carshare:booking_create', kwargs={'vehicle_id': self.v1.id}))
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(reverse('carshare:booking_create', kwargs={'vehicle_id': self.v1.id}), data=form)
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(post_response, 'Sorry, the selected vehicle is unavailable within the chosen times')

    def test_booking_for_time_period_already_booked_by_user_for_different_vehicle(self):
        """
        Booking for a time period that overlaps with an existing booking by the user returns an error message
        """
        form = {
            'booking_start_date': '01/01/3000',
            'booking_start_time': '00:00',
            'booking_end_date': '01/01/3000',
            'booking_end_time': '01:00',
        }
        self.client.login(email='user@test.com', password='bigbadtestuser')
        # First create the valid booking
        get_response = self.client.get(reverse('carshare:booking_create', kwargs={'vehicle_id': self.v1.id}))
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(reverse('carshare:booking_create', kwargs={'vehicle_id': self.v1.id}), data=form)
        booking_id = User.objects.get(email='user@test.com').booking_set.first().id
        self.assertRedirects(post_response, reverse('carshare:booking_detail', kwargs={'booking_id': booking_id}))
        # Then try to create another booking for the same time period but different vehicle
        get_response = self.client.get(reverse('carshare:booking_create', kwargs={'vehicle_id': self.v2.id}))
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(reverse('carshare:booking_create', kwargs={'vehicle_id': self.v2.id}), data=form)
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(post_response, 'Sorry, you already have a booking within the selected time frame')

    def test_booking_detail_with_existing_id(self):
        """
        Booking detail page shows correct booking details for an existing booking
        """
        self.client.login(email='user@test.com', password='bigbadtestuser')
        # Create booking for this user
        form = {
            'booking_start_date': '01/01/3000',
            'booking_start_time': '00:00',
            'booking_end_date': '01/01/3000',
            'booking_end_time': '01:00',
        }
        self.client.login(email='user@test.com', password='bigbadtestuser')
        get_response = self.client.get(reverse('carshare:booking_create', kwargs={'vehicle_id': self.v1.id}))
        self.assertEqual(get_response.status_code, 200)
        self.client.post(reverse('carshare:booking_create', kwargs={'vehicle_id': self.v1.id}),
                                         data=form)
        booking = User.objects.get(email='user@test.com').booking_set.first()
        # Get detail page for the booking
        response = self.client.get(reverse('carshare:booking_detail', kwargs={'booking_id': booking.id}))
        self.assertContains(response, "Booking Detail")
        self.assertContains(response, str(booking.vehicle.make))
        self.assertContains(response, str(booking.vehicle.model))
        self.assertContains(response, str(booking.vehicle.pod.description))
