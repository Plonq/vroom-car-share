from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm, UserProfileForm, AddressForm, CreditCardForm


def register(request):
    if request.user.is_authenticated:
        # User logged in, redirect to profile
        return redirect('profile')

    elif request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        address_form = AddressForm(request.POST)
        credit_card_form = CreditCardForm(request.POST)

        # Validate forms and save
        if user_form.is_valid() and user_profile_form.is_valid() and address_form.is_valid() and credit_card_form.is_valid():
            user = user_form.save()
            user_profile_form.save(commit=False)
            user_profile_form.user = user
            user_profile_form.save()
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
        user_profile_form = UserProfileForm()
        address_form = AddressForm()
        credit_card_form = CreditCardForm()

    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'address_form': address_form,
        'credit_card_form': credit_card_form
    }
    return render(request, 'registration/register.html', context)


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')