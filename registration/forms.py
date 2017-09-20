from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.forms import ModelForm, DateInput
from crispy_forms.helper import FormHelper

from .models import UserProfile, Address, CreditCard
from datetime import date, timedelta


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

    def clean(self):
        # Make sure user is over 18
        cleaned_data = super(UserProfileForm, self).clean()
        date_of_birth = cleaned_data.get("date_of_birth")

        if date_of_birth > date.today() - timedelta(days=18*365):
            self.add_error('date_of_birth', 'You must be over 18 to register.')


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
