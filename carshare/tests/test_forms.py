from django.test import TestCase
from ..forms import *

from django.utils import timezone
from datetime import timedelta


# Handy dates based on current time
two_days_ago = timezone.now() - timedelta(days=2)
yesterday = timezone.now() - timedelta(days=1)
tomorrow = timezone.now() + timedelta(days=1)
two_days_from_now = timezone.now() + timedelta(days=2)


class CarshareBookingFormTests(TestCase):
    def test_valid_form_data(self):
        """
        Booking form with end time after start time is valid
        """
        form_data = {
            'schedule_start': tomorrow,
            'schedule_end': two_days_from_now,
        }
        booking_form = BookingForm(data=form_data)
        self.assertTrue(booking_form.is_valid())

    def test_end_before_start(self):
        """
        Booking form with end time before start time is invalid
        """
        form_data = {
            'schedule_start': two_days_from_now,
            'schedule_end': tomorrow,
        }
        booking_form = BookingForm(data=form_data)
        self.assertFalse(booking_form.is_valid())

    def test_start_time_in_past(self):
        """
        Booking form with start time in the past is invalid
        """
        form_data = {
            'schedule_start': yesterday,
            'schedule_end': tomorrow,
        }
        booking_form = BookingForm(data=form_data)
        self.assertFalse(booking_form.is_valid())