from django.contrib import messages
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import UserCreationSelfForm, AddressForm, CreditCardForm, UserChangeSelfForm
from .models import User, Address


def register_user(request):
    if request.user.is_authenticated:
        # User logged in, redirect to profile
        return redirect('profile')

    # Form submitted, save and redirect to next step
    elif request.method == 'POST':
        user_form = UserCreationSelfForm(request.POST)
        # If user was already created, update existing user
        if 'user_id' in request.session:
            try:
                user_obj = User.objects.get(id=request.session['user_id'])
                user_form.instance = user_obj
                # user_obj.delete()
            except User.DoesNotExist:
                pass
        # Validate forms and save
        if user_form.is_valid():
            # Otherwise save new user, and make inactive for now
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            request.session['user_id'] = user.id

            # Send user to next step
            return redirect('register_address')

    # User maybe pushed back button, display form with saved data
    else:
        if 'user_id' in request.session:
            try:
                user_obj = User.objects.get(id=request.session['user_id'])
                user_form = UserCreationSelfForm(instance=user_obj)
            except ObjectDoesNotExist:
                del request.session['user_info_id']
                user_form = UserCreationSelfForm()

        # Or user just started, display blank form
        else:
            user_form = UserCreationSelfForm()

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
        return redirect('register')

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
        return redirect('register')

    # User hasn't completed step two, redirect to second step
    elif 'address_id' not in request.session:
        return redirect('register_address')

    # User submitted form, save and redirect to next step
    elif request.method == 'POST':
        user_obj = User.objects.get(id=request.session['user_id'])
        credit_card_form = CreditCardForm(request.POST)
        # Validate forms and save
        if credit_card_form.is_valid():
            # Save CC info
            credit_card = credit_card_form.save(commit=False)
            credit_card.user = user_obj
            credit_card.save()

            # Construct and send activation email
            kwargs = {
                "uidb64": urlsafe_base64_encode(force_bytes(user_obj.pk)).decode(),
                "token": default_token_generator.make_token(user_obj)
            }
            activation_url = reverse("activate_account", kwargs=kwargs)
            activate_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), activation_url)
            user_obj.email_user(
                subject='Thank you for joining Vroom!',
                template='registration/email/account_confirmation.html',
                context={
                    'firstname': user_obj.first_name,
                    'activate_url': activate_url
                },
            )

            # Clear registration-related session vars
            del request.session['user_id']
            del request.session['address_id']

            return render(request, 'accounts/activate_request.html')

    # User just came from previous step, display blank form
    else:
        credit_card_form = CreditCardForm()

    # Either brand new form, or form had errors
    context = {
        'credit_card_form': credit_card_form
    }
    return render(request, 'registration/register_credit_card.html', context)


def register_cancel(request):
    try:
        # Must try deleting in this order, because if address doesn't exist, it will skip to except block
        user_obj = User.objects.get(id=request.session['user_id'])
        user_obj.delete()
        del request.session['user_id']
        address_obj = Address.objects.get(id=request.session['address_id'])
        address_obj.delete()
        del request.session['address_id']
    except (User.DoesNotExist, Address.DoesNotExist, KeyError):
        pass


    messages.info(request, 'Registration cancelled')
    return redirect('carshare:index')


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/activate_done.html')
    else:
        return HttpResponse("Activation link has expired")


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserChangeSelfForm(request.POST, instance=user)
        address_form = AddressForm(request.POST, instance=user.address)

        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            address_form.save()

            messages.success(request, 'Changes saved')
            return redirect('profile')
    else:
        user_form = UserChangeSelfForm(instance=user)
        address_form = AddressForm(instance=user.address)

    context = {
        'user_form': user_form,
        'address_form': address_form,
    }

    return render(request, 'accounts/edit_profile.html', context)

@login_required
def update_credit_card(request):
    user = request.user
    if request.method == 'POST':
        credit_card_form = CreditCardForm(request.POST, instance=user.credit_card)

        if credit_card_form.is_valid():
            credit_card_form.save()

            messages.success(request, 'Credit card updated')
            return redirect('edit_profile')
    else:
        # We don't create form from instance because we don't want to display the card details
        credit_card_form = CreditCardForm()

    context = {
        'credit_form': credit_card_form,
    }

    return render(request, 'accounts/update_credit_card.html', context)

# Delete account confirmation, delete if POST
@login_required
def delete_account(request):
    if request.method == 'POST':
        if request.POST['confirm'] == '1':
            request.user.delete()
            return redirect('carshare:index')
    else:
        return render(request, 'accounts/delete_confirmation.html')


# Disable account confirmation, disable if POST
@login_required
def disable_account(request):
    if request.method == 'POST':
        if request.POST['confirm'] == '1':
            request.user.is_active = False
            request.user.save()
            return redirect('carshare:index')
    else:
        return render(request, 'accounts/disable_confirmation.html')
