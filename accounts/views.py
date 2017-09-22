from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm, AddressForm, CreditCardForm, UserChangeSelfForm
from .models import User, Address, CreditCard


def register_user(request):
    if request.user.is_authenticated:
        # User logged in, redirect to profile
        return redirect('profile')

    # Form submitted, save and redirect to next step
    elif request.method == 'POST':
        # If user was already created, delete it first
        try:
            user_obj = User.objects.get(id=request.session['user_id'])
            user_obj.delete()
        except User.DoesNotExist:
            pass
        user_form = UserCreationForm(request.POST)
        # Validate forms and save
        if user_form.is_valid():
            # Otherwise save new user
            user = user_form.save()
            request.session['user_id'] = user.id

            # Send user to next step
            return redirect('register_address')

    # User maybe pushed back button, display form with saved data
    else:
        if 'user_id' in request.session:
            try:
                user_obj = User.objects.get(id=request.session['user_id'])
                user_form = UserCreationForm(instance=user_obj)
            except ObjectDoesNotExist:
                del request.session['user_info_id']
                user_form = UserCreationForm()

        # Or user just started, display blank form
        else:
            user_form = UserCreationForm()

    # Either brand new form, or form had errors
    context = {
        'user_form': user_form,
    }
    return render(request, 'registration/register_user.html', context)


def register_address(request):
    if request.user.is_authenticated:
        # User logged in, redirect to profile
        return redirect('profile')

    # User hasn't completed step one, redirect to first step
    elif 'user_id' not in request.session:
        return redirect('register_user')

    # User submitted form, save and redirect to next step
    elif request.method == 'POST':
        # If address was already created, use it
        if 'address_id' in request.session:
            try:
                address_obj = Address.objects.get(id=request.session['address_id'])
                address_form = AddressForm(request.POST, instance=address_obj)
            except User.DoesNotExist:
                address_form = AddressForm(request.POST)
        else:
            address_form = AddressForm(request.POST)
        # Validate forms and save
        if address_form.is_valid():
            address = address_form.save(commit=False)
            user_obj = User.objects.get(id=request.session['user_id'])
            address.user = user_obj
            address.save()
            request.session['address_id'] = address.id
            return redirect('register_credit_card')

    # User maybe pushed back button, display form with saved data
    else:
        if 'address_id' in request.session:
            try:
                address_obj = Address.objects.get(id=request.session['address_id'])
                address_form = AddressForm(instance=address_obj)
            except ObjectDoesNotExist:
                del request.session['address_id']
                address_form = AddressForm()

        # Or user just came from previous step, display blank form
        else:
            address_form = AddressForm()

    # Either brand new form, or form had errors
    context = {
        'address_form': address_form,
    }
    return render(request, 'registration/register_address.html', context)


def register_credit_card(request):
    if request.user.is_authenticated:
        # User logged in, redirect to profile
        return redirect('profile')

    # User hasn't completed step one, redirect to first step
    elif 'user_id' not in request.session:
        return redirect('register_user')

    # User hasn't completed step two, redirect to second step
    elif 'address_id' not in request.session:
        return redirect('register_address')

    # User submitted form, save and redirect to next step
    elif request.method == 'POST':
        user_obj = User.objects.get(id=request.session['user_id'])
        credit_card_form = CreditCardForm(request.POST)
        # Validate forms and save
        if credit_card_form.is_valid():
            credit_card = credit_card_form.save(commit=False)
            credit_card.user = user_obj
            credit_card.save()

            # Clear registration-related session vars
            del request.session['user_id']
            del request.session['address_id']

            # Auto-login as new user
            login(request, user_obj)
            # TODO: Set success message
            return redirect('profile')

    # User just came from previous step, display blank form
    else:
        credit_card_form = CreditCardForm()

    # Either brand new form, or form had errors
    context = {
        'credit_card_form': credit_card_form
    }
    return render(request, 'registration/register_credit_card.html', context)


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserChangeSelfForm(request.POST, instance=user)
        address_form = AddressForm(request.POST, instance=user.address)
        credit_card_form = CreditCardForm(request.POST, instance=user.credit_card)

        if user_form.is_valid() and address_form.is_valid() and credit_card_form.is_valid():
            user_form.save()
            address_form.save()
            credit_card_form.save()

            return redirect('profile')
    else:
        user_form = UserChangeSelfForm(instance=user)
        address_form = AddressForm(instance=user.address)
        credit_card_form = CreditCardForm(instance=user.credit_card)

    context= {
        'user_form': user_form,
        'address_form': address_form,
        'credit_form': credit_card_form,
    }

    return render(request, 'accounts/edit_profile.html', context)

