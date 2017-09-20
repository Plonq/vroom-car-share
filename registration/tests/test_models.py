from django.test import TestCase
from registration.models import *
import datetime

#
# class UserProfileTestCase(TestCase):
#
#     def test_is_over_18_with_18_year_old(self):
#         """
#         is_over_18() returns True for a user 18 years old
#         """
#         over_18_userprofile = UserProfile(date_of_birth=datetime.date.today() - datetime.timedelta(days=18*365))
#         self.assertTrue(over_18_userprofile.is_over_18())
#
#     def test_is_over_18_with_17_year_old(self):
#         """
#         is_over_18() returns False for a user 17 years and 364 days old
#         """
#         over_18_userprofile = UserProfile(date_of_birth=datetime.date.today() - datetime.timedelta(days=17*365+364))
#         self.assertFalse(over_18_userprofile.is_over_18())