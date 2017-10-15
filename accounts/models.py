from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .managers import UserManager


# Custom User model to use email instead of username
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()

    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Custom user manager
    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth'] # Only used for createsuperuser command

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, template, context, **kwargs):
        """
        Sends an email to this User.
        """
        html_message = render_to_string(template, context)
        text_message = strip_tags(html_message)
        send_mail(
            subject,
            message=text_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            **kwargs
        )

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return self.email

    def get_current_booking(self):
        current_bookings = self.booking_set.all()
        active_bookings = [b for b in current_bookings if b.get_status() == 'Active']
        # Should only ever be one active booking (enforced via validation when creating a booking),
        # but it's technically possible so we always return the first one.
        if active_bookings:
            return active_bookings[0]
        else:
            return None


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
