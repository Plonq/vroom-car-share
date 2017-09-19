from django.shortcuts import render

from .forms import UserForm, AddressForm, CreditCardForm


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        address_form = AddressForm(request.POST)
        credit_card_form = CreditCardForm(request.POST)
        if user_form.is_valid() and address_form.is_valid() and credit_card_form.is_valid():
            user_form.instance.user = request.user
            user = user_form.save()
            usrs = [user_form, address_form, credit_card_form]

            for us in usrs:
                us.save(commit=False)
                us.instance.user = user
                us.save()

        return render(request, 'carshare/index.html')
    else:
        user_form = UserForm()
        address_form = AddressForm()
        credit_card_form = CreditCardForm()

    return render(request, 'registration/register.html', {'user_form': user_form, 'address_form': address_form, 'credit_card_form': credit_card_form})