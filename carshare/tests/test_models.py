from django.test import TestCase

from ..models import *
from datetime import datetime, timedelta


# Create datetime objects relative to now, in order to properly test 'now'-based methods
two_days_ago = datetime.now() - timedelta(days=2)
yesterday = datetime.now() - timedelta(days=1)
tomorrow = datetime.now() + timedelta(days=1)
two_days_from_now = datetime.now() + timedelta(days=2)


class CarshareBookingModelTests(TestCase):
    def test_active_booking(self):
        active_booking = Booking(schedule_start=yesterday, schedule_end=tomorrow)
        self.assertTrue(active_booking.is_active())
        self.assertFalse(active_booking.is_cancelled())
        self.assertFalse(active_booking.is_ended())

    def test_future_booking(self):
        future_booking = Booking(schedule_start=tomorrow, schedule_end=two_days_from_now)
        self.assertFalse(future_booking.is_active())
        self.assertFalse(future_booking.is_cancelled())
        self.assertFalse(future_booking.is_ended())

    def test_ended_booking(self):
        ended_booking = Booking(schedule_start=two_days_ago, schedule_end=yesterday, ended=datetime.now())
        self.assertFalse(ended_booking.is_active())
        self.assertFalse(ended_booking.is_cancelled())
        self.assertTrue(ended_booking.is_ended())

    def test_cancelled_booking(self):
        cancelled_booking = Booking(schedule_start=yesterday, schedule_end=tomorrow, cancelled=datetime.now())
        self.assertFalse(cancelled_booking.is_active())
        self.assertTrue(cancelled_booking.is_cancelled())
        self.assertFalse(cancelled_booking.is_ended())


class CarshareInvoiceModelTests(TestCase):
    def test_non_overdue_invoice(self):
        invoice = Invoice(due=two_days_from_now.date(), amount='56.25')
        self.assertFalse(invoice.is_overdue())
        self.assertEqual(invoice.overdue_days(), 0)

    def test_overdue_invoice(self):
        invoice = Invoice(due=yesterday.date(), amount='56.25')
        self.assertTrue(invoice.is_overdue())
        self.assertEqual(invoice.overdue_days(), 1)