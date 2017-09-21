from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, Address, CreditCard
from datetime import date, timedelta
from .util import is_credit_card_valid, is_digits


# Implement crispy-forms into built-in auth forms
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'date_of_birth')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_date_of_birth(self):
        # Check that DOB indicates user is over 18
        dob = self.cleaned_data.get('date_of_birth')
        if dob > date.today() - timedelta(days=365*18):
            raise forms.ValidationError('You must be 18 years old to sign up')
        return dob

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'date_of_birth',
          )


    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
       return self.initial["password"]

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        del self.fields['password']



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
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["address_line_1", "address_line_2", "city", "state", "postcode"]

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean_postcode(self):
        # Check postcode is exactly 4 digits
        postcode = self.cleaned_data['postcode']
        if len(postcode) != 4 or not is_digits(postcode):
            raise forms.ValidationError('Must be exactly 4 digits')
        return postcode


class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ["card_number", "expiry_month", "expiry_year"]

    def clean_card_number(self):
        # Checks number is valid credit card number
        card_number = self.cleaned_data.get('card_number')
        if not is_credit_card_valid(card_number=card_number):
            raise forms.ValidationError('Must be a valid credit card number')
        return card_number

    def clean_expiry_month(self):
        # Check number is valid month
        expiry_month = self.cleaned_data.get('expiry_month')
        if not (is_digits(expiry_month) and 1 <= int(expiry_month) <= 12):
            raise forms.ValidationError('Must be between 1 and 12 inclusive')
        return expiry_month

    def clean_expiry_year(self):
        # Check number is valid year and that it's at least the current year
        # and no later than 50 years in the future
        expiry_year = self.cleaned_data.get('expiry_year')
        current_year = date.today().year
        if not (is_digits(expiry_year) and current_year <= int(expiry_year) <= (current_year + 50)):
            raise forms.ValidationError('Must not be in the past or later than {0}'.format(current_year + 50))
        return expiry_year

    def clean(self):
        # Check that expiry date is not in the past
        cleaned_data = super(CreditCardForm, self).clean()
        expiry_month = cleaned_data.get('expiry_month')
        expiry_year = cleaned_data.get('expiry_year')
        # Get date objects for first day of month so we can
        # compare only month and year
        t = date.today()
        first_of_month = date(day=1, month=t.month, year=t.year)
        expiry_date = date(day=1, month=int(expiry_month), year=int(expiry_year))
        if expiry_date < first_of_month:
            raise forms.ValidationError('Expiry date must not be in the past')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(CreditCardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False