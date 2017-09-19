from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime


class UserProfile(models.Model):
    """
    Stores user profile information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)

    def is_over_18(self):
        """Returns True if date of birth is at least 18 years in the past to the day"""
        return self.date_of_birth <= datetime.date.today() - datetime.timedelta(days=18*365)


# Signals to create/save UserProfile object when User is created/saved
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=3, choices=STATES)
    postcode = models.CharField(max_length=4)


class CreditCard(models.Model):
    """
    Stores credit card information for a user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='credit_card')
    number = models.CharField(max_length=16)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=4)