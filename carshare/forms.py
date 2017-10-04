from django import forms
from django.utils import timezone

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Field, Fieldset, Button
from crispy_forms.bootstrap import FormActions
from datetimewidget.widgets import DateWidget
import datetime as dt


class ContactForm(forms.Form):
    contact_name = forms.CharField(label='Your name', max_length=60)
    contact_email = forms.EmailField(label='Your email address', max_length=255)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class BookingForm(forms.Form):
    TIMES = (
        ('00:00', '00:00'),
        ('01:00', '01:00'),
        ('02:00', '02:00'),
        ('03:00', '03:00'),
        ('04:00', '04:00'),
        ('05:00', '05:00'),
        ('06:00', '06:00'),
        ('07:00', '07:00'),
        ('08:00', '08:00'),
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('21:00', '21:00'),
        ('22:00', '22:00'),
        ('23:00', '23:00'),
    )
    dateTimeOptions = {
        'format': 'dd/mm/yyyy',
        'startDate': timezone.localtime().date().isoformat(),
    }
    booking_start_date = forms.DateField(widget=DateWidget(options=dateTimeOptions, bootstrap_version=3))
    booking_start_time = forms.ChoiceField(choices=TIMES)
    booking_end_date = forms.DateField(widget=DateWidget(options=dateTimeOptions, bootstrap_version=3))
    booking_end_time = forms.ChoiceField(choices=TIMES)

    def clean_booking_start_time(self):
        booking_start_time = self.cleaned_data.get('booking_start_time')
        # Convert to time object
        booking_start_time = dt.datetime.strptime(booking_start_time, '%H:%M').time()
        return booking_start_time

    def clean_booking_end_time(self):
        booking_end_time = self.cleaned_data.get('booking_end_time')
        # Convert to time object
        booking_end_time = dt.datetime.strptime(booking_end_time, '%H:%M').time()
        return booking_end_time

    def clean(self):
        cleaned_data = super(BookingForm, self).clean()
        if 'booking_start_date' in cleaned_data and 'booking_start_time' in cleaned_data \
            and 'booking_end_date' in cleaned_data and 'booking_end_time' in cleaned_data:
            schedule_start = timezone.make_aware(
                dt.datetime.combine(cleaned_data['booking_start_date'], cleaned_data['booking_start_time']),
                timezone=timezone.get_current_timezone()
            )
            schedule_end = timezone.make_aware(
                dt.datetime.combine(cleaned_data['booking_end_date'], cleaned_data['booking_end_time']),
                timezone=timezone.get_current_timezone()
            )
            # Make sure schedule_end is later than schedule_start
            if schedule_end < schedule_start:
                raise forms.ValidationError('End time must be after the start time')
            # Make sure schedule_start is in the future
            if schedule_start <= timezone.now():
                raise forms.ValidationError('Start time must be in the future')
            # Make sure end is after start (not the same as)
            if schedule_start == schedule_end:
                raise forms.ValidationError('End time must not be the same as the start time')
            # Insert parsed dates into cleaned_data so the view doesn't have to
            cleaned_data['schedule_start'] = schedule_start
            cleaned_data['schedule_end'] = schedule_end
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'validated-form'
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Booking Start',
                Div(
                    Div(
                        Field('booking_start_date', css_class='datepicker', placeholder='Date'),
                        css_class='col-sm-8',
                    ),
                    Div(
                        'booking_start_time',
                        css_class='col-sm-4',
                    ),
                    css_class='row',
                )
            ),
            Fieldset('Booking End',
                Div(
                    Div(
                        Field('booking_end_date', css_class='datepicker', placeholder='Date'),
                        css_class='col-sm-8',
                    ),
                    Div(
                        'booking_end_time',
                        css_class='col-sm-4',
                    ),
                    css_class='row',
                )
            )
        )


class ExtendBookingForm(forms.Form):
    """
    Form for extending a booking
    """
    dateTimeOptions = {
        'format': 'dd/mm/yyyy',
    }
    booking_start_date = forms.DateField()
    booking_start_time = forms.ChoiceField(choices=BookingForm.TIMES)

    def __init__(self, *args, **kwargs):
        super(ExtendBookingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # Set date and time fields minimum to current booking end datetime
        self.min_datetime = kwargs.pop('min_datetime')
        self.dateTimeOptions['startDate'] = self.min_datetime.date().isoformat()
        self.fields['booking_start_date'].widget = DateWidget(options=self.dateTimeOptions, bootstrap_version=3)