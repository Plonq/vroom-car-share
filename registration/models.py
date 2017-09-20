from django.db import models
from django.contrib.auth.models import User

import datetime


class UserProfile(models.Model):
    """
    Stores user profile information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # All fields must be optional (null=True blank=True) since this object will be created and saved with the user
    date_of_birth = models.DateField()

    def is_over_18(self):
        """Returns True if date of birth is at least 18 years in the past to the day"""
        return self.date_of_birth <= datetime.date.today() - datetime.timedelta(days=18*365)

    def __str__(self):
        # Appears on django-admin
        return self.user.username


class Address(models.Model):
    """
    Stores an address for a user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')

    STATES = (
        ('VIC', 'Victoria'),
        ('NSW', 'New South Wales'),
        ('WA', 'Western Australia'),
        ('TAS', 'Tasmania'),
        ('QLD', 'Queensland'),
        ('SA', 'South Australia'),
    )
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=3, choices=STATES)
    postcode = models.CharField(max_length=4)

    def __str__(self):
        return "{0}, {1}, {2} {3}".format(self.address_line_1, self.city, self.state, self.postcode)


class CreditCard(models.Model):
    """
    Stores credit card information for a user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='credit_card')
    card_number = models.CharField(max_length=16)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=4)

    def __str__(self):
        return "XXXX XXXX XXXX {0}".format(self.card_number[-4:])