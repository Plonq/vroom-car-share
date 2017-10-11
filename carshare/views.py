from django.contrib import messages
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

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
def booking_create(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

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
                if (b.schedule_start <= booking_start <= b.schedule_end or
                    b.schedule_start <= booking_end <= b.schedule_end or
                    booking_start <= b.schedule_start and booking_end >= b.schedule_end):
                    is_valid_booking = False
                    booking_form.add_error(None, "Sorry, the selected vehicle is unavailable within the chosen times")
                    break
            # Prevent multiple bookings for the same user during the same time period
            user_bookings = request.user.booking_set.all()
            for b in user_bookings:
                if (b.schedule_start <= booking_start <= b.schedule_end or
                    b.schedule_start <= booking_end <= b.schedule_end or
                    booking_start <= b.schedule_start and booking_end >= b.schedule_end):
                    is_valid_booking = False
                    booking_form.add_error(None, "Sorry, you already have a booking within the selected time frame")
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
        booking_form = BookingForm()

    context = {
        'vehicle': vehicle,
        'booking_form': booking_form,
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
def booking_index(request):
    bookings = request.user.booking_set.all().order_by('-schedule_start')
    context = {
        'bookings': bookings,
    }
    return render(request, "carshare/bookings/index.html", context)


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
