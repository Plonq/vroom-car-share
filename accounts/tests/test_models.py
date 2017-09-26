from django.core import mail
from django.test import TestCase

from ..models import *


class AccountsUserModelTests(TestCase):
    user = User(email='test@test.com', first_name='John', last_name='Doe', date_of_birth='2017-01-01')

    def test_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'John Doe')

    def test_short_name(self):
        self.assertEqual(self.user.get_short_name(), 'John')

    def test_email_user(self):
        self.user.email_user('Subject', 'Message', 'testrunner@test.com')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject')
        self.assertEqual(mail.outbox[0].body, 'Message')
        self.assertEqual(mail.outbox[0].from_email, 'testrunner@test.com')


class AccountsAddressModelTests(TestCase):
    address = Address(address_line_1='Address Line 1', address_line_2='Address Line 2', city='City', state='VIC',
                      postcode='3000')

    def test_string_output(self):
        self.assertEqual(self.address.__str__(), 'Address Line 1, City, VIC 3000')


class AccountsCreditCardModelTests(TestCase):
    credit_card = CreditCard(card_number='1111222233334444')

    def test_string_output(self):
        self.assertEqual(self.credit_card.__str__(), 'XXXX XXXX XXXX 4444')