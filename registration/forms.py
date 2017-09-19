from django.forms import ModelForm
from registration.models import UserProfile, Address, CreditCard
class UserForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('username',)

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ("address_line1", "city", "state", "postcode")


class CreditCardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = ("number", "expiry_month", "expiry_year")

