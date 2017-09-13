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