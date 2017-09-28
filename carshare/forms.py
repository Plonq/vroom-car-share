from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Button, Submit, Field
from crispy_forms.bootstrap import FormActions
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


class BookingForm(forms.Form):
    booking_start_date = forms.DateField()
    booking_start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    booking_end_date = forms.DateField()
    booking_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

        # dateTimeOptions = {
        #     'format': 'yyyy-mm-dd hh:00',
        #     'minView': 1,
        #     'minuteStep': 60,
        #     'startDate': timezone.now().date().isoformat(),
        # }
        # widgets = {
        #     'booking_start_date': ,
        #     'booking_start_time': ,
        # }

    # def clean(self):
    #     cleaned_data = super(BookingForm, self).clean()
    #     schedule_start = cleaned_data.get('schedule_start')
    #     schedule_end = cleaned_data.get('schedule_end')
    #     if schedule_start and schedule_end:
    #         # Make sure schedule_end is later than schedule_start
    #         if schedule_end < schedule_start:
    #             raise forms.ValidationError('End time must be after the start time')
    #         # Make sure schedule_start is in the future
    #         if schedule_start <= timezone.now():
    #             raise forms.ValidationError('Start time must be in the future')
    #         # TODO Prevent time overlapping with existing booking
    #     return cleaned_data

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'validated-form'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('booking_start_date', css_class='datepicker'),
                    css_class='col-sm-5',
                ),
                Div(
                    'booking_start_time',
                    css_class='col-sm-5',
                ),
                css_class='row',
            ),
            Div(
                Div(
                    Field('booking_end_date', css_class='datepicker'),
                    css_class='col-sm-5',
                ),
                Div(
                    'booking_end_time',
                    css_class='col-sm-5',
                ),
                css_class='row',
            ),
            FormActions(
                Submit('submit', 'Book', css_class='btn btn-primary'),
            )
        )