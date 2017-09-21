from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm, UserChangeForm
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, Address, CreditCard


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
# class UserProfileForm(form.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['date_of_birth']
#         widgets = {
#             'date_of_birth': DateInput(attrs={'type': 'date'})
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_tag = False
#
#     def clean(self):
#         # Make sure user is over 18
#         cleaned_data = super(UserProfileForm, self).clean()
#         date_of_birth = cleaned_data.get("date_of_birth")
#
#         if date_of_birth > date.today() - timedelta(days=18*365):
#             self.add_error('date_of_birth', 'You must be over 18 to register.')


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["address_line_1", "address_line_2", "city", "state", "postcode"]

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ["card_number", "expiry_month", "expiry_year"]

    def __init__(self, *args, **kwargs):
        super(CreditCardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


#Contact Form

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)



