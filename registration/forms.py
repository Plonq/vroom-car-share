from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.forms import ModelForm, DateInput
from crispy_forms.helper import FormHelper

from .models import UserProfile, Address, CreditCard


# Implement crispy-forms into built-in auth forms
class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class AuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


# Auth ModelForms with crispy-forms
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ["address_line_1", "address_line_2", "city", "state", "postcode"]

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class CreditCardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = ["card_number", "expiry_month", "expiry_year"]

    def __init__(self, *args, **kwargs):
        super(CreditCardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
