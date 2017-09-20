from django.forms import ModelForm
from crispy_forms.helper import FormHelper

from .models import UserProfile, Address, CreditCard


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ["address_line1", "city", "state", "postcode"]

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()


class CreditCardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = ["number", "expiry_month", "expiry_year"]

    def __init__(self, *args, **kwargs):
        super(CreditCardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
