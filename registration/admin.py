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
        # Prevents profile fields when creating new user or if user is staff
        if not obj or obj.is_staff:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

    def get_readonly_fields(self, request, obj=None):
        # Prevent staff changing their own permissions
        rof = super(UserAdmin, self).get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            rof += ('is_staff', 'is_superuser', 'groups', 'user_permissions')
        return rof

    def has_change_permission(self, request, obj=None):
        # Prevent staff changing other user's who may have higher privileges.
        has = super(UserAdmin, self).has_change_permission(request, obj)
        if obj and not request.user.is_superuser:
            if obj != request.user:
                if obj.is_superuser or obj.user_permissions.exists():
                    has = False
        return has

# Re-register user admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
