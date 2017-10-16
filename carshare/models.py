from django.db import models
from django.utils import timezone

from decimal import Decimal
from accounts.models import User
from datetime import timedelta


class VehicleType(models.Model):
    """
    Types and costs of vehicles
    """
    description = models.CharField(max_length=30)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "{0} - Hourly: ${1:.2f} Daily: ${2:.2f}".format(self.description, float(self.hourly_rate), float(self.daily_rate))


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
        str = "{0}".format(self.description)
        if hasattr(self, 'vehicle'):
            str += " ({0})".format(self.vehicle.name)
        return str


class Vehicle(models.Model):
    """
    A Vroom vehicle
    """
    type = models.ForeignKey(VehicleType, related_name='type')
    pod = models.OneToOneField(Pod, null=True, blank=True)
    name = models.CharField(max_length=30, unique=True)
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=True)
    registration = models.CharField(max_length=6, unique=True)

    def is_active(self):
        return self.active

    def is_available(self):
        """
        Is the vehicle available for booking right now?
        """
        current_bookings = self.booking_set.all()
        active_bookings = [b for b in current_bookings if b.is_active()]
        if not active_bookings:
            return True
        else:
            return False

    def is_available_at(self, datetime):
        """
        Checks if the vehicle is available at the time specified
        :param datetime: when to check
        :return: Boolean
        """
        for booking in self.booking_set.all():
            if (booking.schedule_start <= datetime < booking.schedule_end and
                booking.get_status() != 'Cancelled' and
                booking.get_status() != 'Ended'):
                return False
        return True

    def __str__(self):
        # E.g. 'Jackie - 2014 Toyota Corolla'
        return "{0} - {1} {2} {3}".format(self.name, self.year, self.make, self.model)


class Booking(models.Model):
    """
    Details about particular booking by a user for a vehicle
    """
    user = models.ForeignKey(User)
    vehicle = models.ForeignKey(Vehicle)
    schedule_start = models.DateTimeField(verbose_name='Start time')
    schedule_end = models.DateTimeField(verbose_name='End time')
    ended = models.DateTimeField(null=True, blank=True)
    cancelled = models.DateTimeField(null=True, blank=True)


    def is_active(self):
        return (
            # We add an hour to the current time, because if it's e.g. 9:15 and a car is booked from
            # 10:00 to 11:00, the user cannot book it right now (can't choose 10:00 as it's in the past)
            # TODO: Update this if we decide to do half-hour bookings
            self.schedule_start < (timezone.now() + timedelta(hours=1)) < self.schedule_end and
            self.ended is None and
            self.cancelled is None
        )

    def is_cancelled(self):
        return self.cancelled is not None

    def calculate_cost(self):
        """
        Calculates total cost of booking, taking into account hourly rate and daily rate of the vehicle
        :return: float
        """
        booking_length = self.schedule_end - self.schedule_start
        booking_length_hours_total = booking_length.days * 24 + booking_length.seconds / 60 / 60
        booking_days = int(booking_length_hours_total / 24)
        booking_hours = int(booking_length_hours_total % 24)
        return float(
            (booking_days * Decimal(self.vehicle.type.daily_rate)) +
            (booking_hours * Decimal(self.vehicle.type.hourly_rate))
        )

    def is_ended(self):
        return self.ended is not None

    def get_status(self):
        """
        Returns a string indicating the status
        """
        if self.ended:
            return "Ended"
        elif self.cancelled:
            return "Cancelled"
        elif self.schedule_start > timezone.now():
            return "Confirmed"
        elif self.schedule_start < timezone.now() < self.schedule_end:
            return "Active"
        elif self.schedule_end < timezone.now():
            return "Expired"

    def __str__(self):
        return str(self.id)


class Invoice(models.Model):
    """
    Invoice for a single booking
    """
    booking = models.OneToOneField(Booking, related_name='invoice')
    date = models.DateField(default=timezone.now)
    due = models.DateField()
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    paid = models.BooleanField(default=False)

    def is_overdue(self):
        return self.due < timezone.now().date()

    def overdue_days(self):
        """
        Number of days overdue, or 0 if not overdue
        """
        if not self.is_overdue():
            return 0
        else:
            return (timezone.now().date() - self.due).days

