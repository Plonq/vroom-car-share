from django import forms

from crispy_forms.helper import FormHelper
from datetimewidget.widgets import DateTimeWidget

from .models import Booking
from django.utils import timezone


class ContactForm(forms.Form):
    contact_name = forms.CharField(label='Your name', max_length=60)
    contact_email = forms.EmailField(label='Your email address', max_length=255)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["schedule_start", "schedule_end"]

        dateTimeOptions = {
            'format': 'yyyy-mm-dd hh:00',
            'minView': 1,
            'minuteStep': 60,
            'startDate': timezone.now().date().isoformat(),
        }
        widgets = {
            'schedule_start': DateTimeWidget(bootstrap_version=3, options=dateTimeOptions),
            'schedule_end': DateTimeWidget(bootstrap_version=3, options=dateTimeOptions),
        }

    def clean(self):
        cleaned_data = super(BookingForm, self).clean()
        schedule_start = cleaned_data.get('schedule_start')
        schedule_end = cleaned_data.get('schedule_end')
        if schedule_start and schedule_end:
            # Make sure schedule_end is later than schedule_start
            if schedule_end < schedule_start:
                raise forms.ValidationError('End time must be after the start time')
            # Make sure schedule_start is in the future
            if schedule_start <= timezone.now():
                raise forms.ValidationError('Start time must be in the future')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False