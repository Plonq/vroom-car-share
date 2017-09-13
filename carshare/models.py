from django.db import models
from django.contrib.auth.models import User
import datetime


class Driver(models.Model):
    """
    Stores extra information about users that are also drivers (customers)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()

    def is_over_18(self):
        """Returns True if date of birth is at least 18 years in the past to the day"""
        return self.date_of_birth <= datetime.date.today() - datetime.timedelta(days=18*365)