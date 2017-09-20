from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Address, CreditCard
from .forms import UserCreationForm, UserChangeForm

#
# User and its related profile models (UserProfile, Address, CreditCard)
#

# Inline admin descriptors
# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'Profile'


class AddressInline(admin.StackedInline):
    model = Address
    can_delete = True
    verbose_name_plural = 'Address'


class CreditCardInline(admin.StackedInline):
    model = CreditCard
    can_delete = True
    verbose_name_plural = 'Credit Card'


class UserAdmin(BaseUserAdmin):
    # Add inline forms for address and credit card
    inlines = (AddressInline, CreditCardInline)

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

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


# Register user admin
admin.site.register(User, UserAdmin)
