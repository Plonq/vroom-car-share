from django.contrib import messages
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ContactForm, BookingForm
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

def findacar(request):
    active_vehicles_with_pods = Vehicle.objects.filter(active=True).exclude(pod__isnull=True)
    context = {
        'vehicles': active_vehicles_with_pods
    }
    return render(request, "carshare/findacar.html", context)

@login_required
def new_booking(request, vehicle_name):
    vehicle = Vehicle.objects.get(name__iexact=vehicle_name)

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            # Process form and create booking
            booking = booking_form.save(commit=False)
            print(booking.schedule_start)
            booking.user = request.user
            booking.vehicle = vehicle
            booking.save()

            messages.success(request, 'Booking created successfully')
            return redirect('booking_detail', booking.pk)
    else:
        booking_form = BookingForm()

    context = {
        'vehicle': vehicle,
        'booking_form': booking_form,
    }
    return render(request, "carshare/bookings/create.html", context)

@login_required
def booking_detail(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    if request.user != booking.user:
        messages.error(request, 'You do not have permission to view that booking')
        return redirect('index')
    context = {
        'booking': booking,
    }
    return render(request, "carshare/bookings/detail.html", context)
