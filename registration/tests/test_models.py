from django.test import TestCase
from registration.models import *
import datetime


class UserProfileTestCase(TestCase):

    def test_user_profile_created_when_user_created(self):
        """
        UserProfile correctly created when a User is created
        """
        user = User.objects.create()
        self.assertNotEqual(User.objects.get(pk=user.pk).profile, None)

    def test_user_profile_saved_when_user_saved(self):
        """
        UserProfile correctly created when a User is created
        """
        dob = datetime.date(2017, 9, 14)
        user = User.objects.create()
        user.profile.date_of_birth = dob
        user.save()
        self.assertEqual(User.objects.get(pk=user.pk).profile.date_of_birth, dob)

    def test_is_over_18_with_18_year_old(self):
        """
        is_over_18() returns True for a user 18 years old
        """
        over_18_userprofile = UserProfile(date_of_birth=datetime.date.today() - datetime.timedelta(days=18*365))
        self.assertTrue(over_18_userprofile.is_over_18())

    def test_is_over_18_with_17_year_old(self):
        """
        is_over_18() returns False for a user 17 years and 364 days old
        """
        over_18_userprofile = UserProfile(date_of_birth=datetime.date.today() - datetime.timedelta(days=17*365+364))
        self.assertFalse(over_18_userprofile.is_over_18())


class AddressTestCase(TestCase):

    def test_address_created_when_user_created(self):
        """
        Address correctly created when a User is created
        """
        user = User.objects.create()
        self.assertNotEqual(User.objects.get(pk=user.pk).address, None)

    def test_address_saved_when_user_saved(self):
        """
        Address correctly created when a User is created
        """
        city = 'testing'
        user = User.objects.create()
        user.address.city = city
        user.save()
        self.assertEqual(User.objects.get(pk=user.pk).address.city, city)


class CreditCardTestCase(TestCase):

    def test_credit_card_created_when_user_created(self):
        """
        CreditCard correctly created when a User is created
        """
        user = User.objects.create()
        self.assertNotEqual(User.objects.get(pk=user.pk).credit_card, None)

    def test_credit_card_saved_when_user_saved(self):
        """
        CreditCard correctly created when a User is created
        """
        number = '1111222233334444'
        user = User.objects.create()
        user.credit_card.number = number
        user.save()
        self.assertEqual(User.objects.get(pk=user.pk).credit_card.number, number)