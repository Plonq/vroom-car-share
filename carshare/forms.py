from django import forms
from crispy_forms.helper import FormHelper

class ContactForm(forms.Form):
    contact_name = forms.CharField(label='Your name', max_length=60)
    contact_email = forms.EmailField(label='Your email address', max_length=255)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
