from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from registration.models import UserProfile, Address, CreditCard

#
# User and its related profile models (UserProfile, Address, CreditCard)
#

# Inline admin descriptors
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class AddressInline(admin.StackedInline):
    model = Address
    can_delete = True
    verbose_name_plural = 'Address'


class CreditCardInline(admin.StackedInline):
    model = CreditCard
    can_delete = True
    verbose_name_plural = 'Credit Card'


# Define new UserAdmin, containing above inlines
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, AddressInline, CreditCardInline)

    def get_inline_instances(self, request, obj=None):
        """Prevents profile fields when creating new user"""
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

# Re-register user admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
