from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from carshare.forms import ContactForm

# Create your views here.
def index(request):
    return render(request, 'carshare/index.html')

def email(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@vroomcs.org'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, "carshare/contactus_success.html")
    return render(request, "carshare/contactus.html", {'form': form})
