from django.test import TestCase
from carshare.models import *
import datetime


class DriverTestCase(TestCase):

    def test_is_over_18_with_18_year_old(self):
        """
        is_over_18() returns True for a Driver 18 years old
        """
        over_18_driver = Driver(date_of_birth=datetime.date.today() - datetime.timedelta(days=18*365))
        self.assertTrue(over_18_driver.is_over_18())

    def test_is_over_18_with_17_year_old(self):
        """
        is_over_18() returns False for a Driver 17 years and 364 days old
        """
        over_18_driver = Driver(date_of_birth=datetime.date.today() - datetime.timedelta(days=17*365+364))
        self.assertFalse(over_18_driver.is_over_18())

    def test_driver_user_relation(self):
        """
        driver.user returns correct related User
        """
        user = User.objects.create(username='test_driver_user_relation')
        user.save()
        driver_with_user = Driver.objects.create(date_of_birth=datetime.date.today(), user=user)
        driver_with_user.save()
        self.assertEqual(Driver.objects.get(pk=driver_with_user.pk).user, User.objects.get(username='test_driver_user_relation'))

    def test_user_driver_relation(self):
        """
        user.driver returns correct related Driver
        """
        user = User.objects.create(username='test_user_driver_relation')
        user.save()
        driver_with_user = Driver.objects.create(date_of_birth=datetime.date.today(), user=user)
        driver_with_user.save()
        self.assertEqual(Driver.objects.get(pk=driver_with_user.pk), User.objects.get(pk=user.pk).driver)