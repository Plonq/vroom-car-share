from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm

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

    contact_form = ContactForm()
    return render(request, "carshare/contact_us.html", {'contact_form': contact_form})
