from django.forms import ModelForm

from .models import UserProfile, Address, CreditCard


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('date_of_birth',)


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ("address_line1", "city", "state", "postcode")


class CreditCardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = ("number", "expiry_month", "expiry_year")

