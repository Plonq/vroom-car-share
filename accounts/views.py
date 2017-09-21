from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, AddressForm, CreditCardForm, UserChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def register(request):
    if request.user.is_authenticated:
        # User logged in, redirect to profile
        return redirect('profile')

    elif request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        address_form = AddressForm(request.POST)
        credit_card_form = CreditCardForm(request.POST)
        # Validate forms and save
        if user_form.is_valid() and address_form.is_valid() and credit_card_form.is_valid():
            user = user_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            credit_card = credit_card_form.save(commit=False)
            credit_card.user = user
            credit_card.save()

            # Auto-login as new user
            login(request, user)

            return redirect('profile')

    else:
        user_form = UserCreationForm()
        address_form = AddressForm()
        credit_card_form = CreditCardForm()

    context = {
        'user_form': user_form,
        'address_form': address_form,
        'credit_card_form': credit_card_form
    }
    return render(request, 'registration/register.html', context)


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


def editprofile(request):
    user = request.user
    if request.method == 'POST':

        user_form = UserChangeForm(request.POST, instance= user,
                                   initial={'first_name': user.first_name, 'last_name': user.last_name,
                                            'email': user.email,
                                            'password': user.password})

        address_form = AddressForm(request.POST, instance= user.address,
                                   initial={'address_line1': user.address.address_line_1,
                                                                  'address_line2': user.address.address_line_2,
                                                                  'city': user.address.city,
                                                                  'state': user.address.state,
                                                                  'postcode': user.address.postcode})

        credit_form = CreditCardForm(request.POST, instance=user.credit_card,
                                   initial={'card_number': user.credit_card.card_number,
                                                                'expiry_month': user.credit_card.expiry_month,
                                                                'expiry_year': user.credit_card.expiry_year})

        if user_form.is_valid() and address_form.is_valid():
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.address.address_line_1 = request.POST['address_line_1']
            user.address.address_line_2 = request.POST['address_line_2']
            user.address.city = request.POST['city']
            user.address.state = request.POST['state']
            user.address.postcode = request.POST['postcode']
            user.credit_card.card_number = request.POST['card_number']
            user.credit_card.expiry_month = request.POST['expiry_month']
            user.credit_card.expiry_year = request.POST['expiry_year']
            user.save()
            user.address.save()
            user.credit_card.save()
            return redirect('profile')
    else:
        user_form = UserChangeForm(instance=user)
        address_form = AddressForm(instance=user.address)
        credit_form = CreditCardForm(instance=user.credit_card)
    context= {
        'user_form': user_form,
        'address_form': address_form,
        'credit_form': credit_form,
    }

    return render(request, 'accounts/editprofile.html', context)

