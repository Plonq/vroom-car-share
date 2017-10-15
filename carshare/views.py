from django.contrib import messages
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

import datetime as dt

from .forms import ContactForm, BookingForm, ExtendBookingForm
from .models import Vehicle, Booking


# Create your views here.
def index(request):
    return render(request, 'carshare/index.html')


def contact_us(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_name = contact_form.cleaned_data['contact_name']
            contact_email = contact_form.cleaned_data['contact_email']
            subject = 'New Contact Us from {0}'.format(contact_name)
            message = contact_form.cleaned_data['message']
            try:
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email='admin@vroomcs.org',
                    to=['admin@vroomcs.org'],
                    reply_to=[contact_email],
                )
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, "carshare/contact_us_success.html")
    else:
        contact_form = ContactForm()

    return render(request, "carshare/contact_us.html", {'contact_form': contact_form})


def find_a_car(request):
    active_vehicles_with_pods = Vehicle.objects.filter(active=True).exclude(pod__isnull=True)
    context = {
        'vehicles': active_vehicles_with_pods
    }
    return render(request, "carshare/find_a_car.html", context)


@login_required
def booking_timeline(request, vehicle_id, year=None, month=None, day=None):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    # Default to today if no date specified
    if year and month and day:
        date = dt.date(int(year), int(month), int(day))
    else:
        date = timezone.localtime().date()
    # Build dict of hours and whether that hour is available
    hours = {}
    for i in range(0, 24):
        datetime = timezone.make_aware(dt.datetime.combine(date, dt.time(hour=i, minute=0)), timezone.get_current_timezone())
        if vehicle.is_available_at(datetime=datetime) and datetime > timezone.localtime():
            hours[i] = 'available'
        else:
            hours[i] = 'unavailable'
    context = {
        'vehicle': vehicle,
        'hours': hours,
        'date': date,
        'today': timezone.localtime().today().date(),
    }
    return render(request, "carshare/bookings/create_timeline.html", context)


@login_required
def booking_create(request, vehicle_id, year=None, month=None, day=None, hour=None):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    datetime = dt.datetime(int(year), int(month), int(day), int(hour), minute=0)

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            data = booking_form.cleaned_data
            booking_start = data['schedule_start']
            booking_end = data['schedule_end']

            # Custom validation
            is_valid_booking = True
            # Prevent booking overlapping with existing booking
            existing_bookings = Booking.objects.filter(vehicle=vehicle)
            for b in existing_bookings:
                if (b.schedule_start <= booking_start < b.schedule_end or
                    b.schedule_start < booking_end <= b.schedule_end or
                    booking_start <= b.schedule_start and booking_end >= b.schedule_end):
                    is_valid_booking = False
                    booking_form.add_error(None, "The selected vehicle is unavailable within the chosen times")
                    break
            # Prevent multiple bookings for the same user during the same time period
            user_bookings = request.user.booking_set.all()
            for b in user_bookings:
                if (b.schedule_start <= booking_start < b.schedule_end or
                    b.schedule_start < booking_end <= b.schedule_end or
                    booking_start <= b.schedule_start and booking_end >= b.schedule_end):
                    is_valid_booking = False
                    booking_form.add_error(None, "You already have a booking within the selected time frame")
                    break

            if is_valid_booking:
                # Process form and create booking
                booking = Booking(
                    user=request.user,
                    vehicle=vehicle,
                    schedule_start=booking_start,
                    schedule_end=booking_end,
                )
                booking.save()

                # Send confirmation email
                request.user.email_user(
                    subject='Booking confirmed!',
                    template='carshare/email/booking_confirmation.html',
                    context={
                        'firstname': request.user.first_name,
                        'booking': booking,
                    },
                )

                messages.success(request, 'Booking created successfully')
                return redirect('carshare:booking_detail', booking.pk)
            # Else, continue and render the same page with form errors
    else:
        booking_form = BookingForm(initial_start_datetime=datetime)
        booking_form.is_bound = False  # Prevent validation triggering

    context = {
        'vehicle': vehicle,
        'booking_form': booking_form,
        'date': datetime.date,
    }
    return render(request, "carshare/bookings/create.html", context)


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.user != booking.user:
        messages.error(request, 'You do not have permission to view that booking')
        return redirect('carshare:index')
    context = {
        'booking': booking,
    }
    return render(request, "carshare/bookings/detail.html", context)


@login_required
def my_bookings(request):
    now = timezone.localtime()
    midnight = timezone.make_aware(dt.datetime(now.year, now.month, now.day), timezone=timezone.get_current_timezone()) + dt.timedelta(days=1)
    today_bookings = request.user.booking_set.filter(schedule_start__gte=now, schedule_start__lte=midnight).order_by('-schedule_start')
    current_booking = request.user.get_current_booking()
    upcoming_bookings = request.user.booking_set.filter(schedule_start__gt=midnight).order_by('-schedule_start')
    past_bookings = request.user.booking_set.filter(schedule_end__lte=now).order_by('schedule_start')
    context = {
        'today_bookings': today_bookings,
        'current_booking': current_booking,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
    }
    return render(request, "carshare/bookings/my_bookings.html", context)


@login_required
def booking_extend(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.user != booking.user:
        messages.error(request, 'You do not have permission to view that booking')
        return redirect('carshare:index')

    if request.method == 'POST':
        extend_booking_form = ExtendBookingForm(request.POST, current_booking_end=booking.schedule_end)
        if extend_booking_form.is_valid():
            new_schedule_end = extend_booking_form.cleaned_data['new_schedule_end']
            # Custom validation
            is_valid_booking = True
            # Make sure new end date doesn't clash with existing booking
            existing_bookings = Booking.objects.filter(vehicle=booking.vehicle).exclude(user=request.user)
            for b in existing_bookings:
                if (b.schedule_start <= booking.schedule_start <= b.schedule_end or
                    b.schedule_start <= new_schedule_end <= b.schedule_end or
                    booking.schedule_start <= b.schedule_start and new_schedule_end >= b.schedule_end):
                    is_valid_booking = False
                    extend_booking_form.add_error(None, "The new end date overlaps with existing booking. "
                                                        "The latest date you can choose is {0}".format(b.schedule_start))
                    break
            user_bookings = request.user.booking_set.exclude(id__exact=booking.id)
            for b in user_bookings:
                if (b.schedule_start <= booking.schedule_start <= b.schedule_end or
                    b.schedule_start <= new_schedule_end <= b.schedule_end or
                    booking.schedule_start <= b.schedule_start and new_schedule_end >= b.schedule_end):
                    is_valid_booking = False
                    extend_booking_form.add_error(
                        None, "The new booking end overlaps with one of your existing bookings"
                    )
                    break

            if is_valid_booking:
                booking.schedule_end = new_schedule_end
                booking.save()

                # Send confirmation email TODO: create new template
                request.user.email_user(
                    subject='Booking extended',
                    template='carshare/email/booking_extend_confirmation.html',
                    context={
                        'firstname': request.user.first_name,
                        'booking': booking,
                    },
                )

                messages.success(
                    request, "Your current booking has been extended. You will receive email confirmation shortly."
                )
                return redirect('carshare:booking_detail', booking_id)
    else:
        extend_booking_form = ExtendBookingForm(current_booking_end=booking.schedule_end)

    context = {
        'booking': booking,
        'extend_booking_form': extend_booking_form,
    }
    return render(request, "carshare/bookings/extend.html", context)

def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.user != booking.user:
        messages.error(request, 'You do not have permission to view that booking')
        return redirect('carshare:index')
    booking.cancelled = timezone.now()
    booking.save()
    messages.success(request,'Successfully cancelled booking for {0} the {1} {2}'.format(booking.vehicle.name,
                                                                                         booking.vehicle.make,
                                                                                         booking.vehicle.model))
    return redirect('carshare:my_bookings')


def booking_end(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.user != booking.user:
        messages.error(request, 'You do not have permission to view that booking')
        return redirect('carshare:index')
    # Only allow to end booking if the booking is active.
    if booking.get_status() == 'Active':
        booking.ended = timezone.now()
        booking.save()
        messages.success(request, 'Your booking has ended')
    else:
        # Request them to Cancel booking rather than end.
        messages.error(request, 'You cannot end this booking as it has not started yet. Please cancel instead.')
        return redirect('carshare:booking_detail', booking.id)
    return redirect('carshare:my_bookings')
