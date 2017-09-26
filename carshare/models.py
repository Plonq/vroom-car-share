from django.db import models

from accounts.models import User
from datetime import date, datetime


class VehicleType(models.Model):
    """
    Types and costs of vehicles
    """
    description = models.CharField(max_length=30)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "{0}: ${1}".format(self.description, self.hourly_rate)


class Pod(models.Model):
    """
    A designated/reserved parking spot for Vroom vehicles
    """
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    description = models.CharField(max_length=200)

    def coordinates(self):
        return "{0},{1}".format(self.latitude, self.longitude)

    def __str__(self):
        return self.description


class Vehicle(models.Model):
    """
    A Vroom vehicle
    """
    type = models.ForeignKey(VehicleType, related_name='type')
    pod = models.OneToOneField(Pod)
    name = models.CharField(max_length=30)
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=True)

    def is_active(self):
        return self.active

    def __str__(self):
        # Jackie - 2014 Toyota Corolla
        return "{0} - {1} {2} {3}".format(self.name, self.year, self.make, self.model)


class Booking(models.Model):
    """
    Details about particular booking by a user for a vehicle
    """
    user = models.ForeignKey(User, related_name='user')
    vehicle = models.ForeignKey(Vehicle, related_name='vehicle')
    schedule_start = models.DateTimeField()
    schedule_end = models.DateTimeField()
    ended = models.DateTimeField(null=True, blank=True)
    cancelled = models.DateTimeField(null=True, blank=True)

    def is_active(self):
        return (
            self.schedule_start < datetime.now() < self.schedule_end and
            self.ended is None and
            self.cancelled is None
        )

    def is_cancelled(self):
        return self.cancelled is not None

    def is_ended(self):
        return self.ended is not None


class Invoice(models.Model):
    """
    Invoice for a single booking
    """
    booking = models.OneToOneField(Booking, related_name='booking')
    date = models.DateField(default=date.today)
    due = models.DateField()
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def is_overdue(self):
        return self.due < date.today()

    def overdue_days(self):
        """
        Number of days overdue, or 0 if not overdue
        """
        if not self.is_overdue():
            return 0
        else:
            return (date.today() - self.due).days