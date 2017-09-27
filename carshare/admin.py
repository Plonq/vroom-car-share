from django.contrib import admin

from .models import Vehicle, Pod, VehicleType


def make_active(modeladmin, request, queryset):
    queryset.update(active=True)
make_active.short_description = "Mark selected vehicles as active"

def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)
make_inactive.short_description = "Mark selected vehicles as inactive"

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'make', 'model', 'pod', 'active']
    ordering = ['name']
    actions = [make_active, make_inactive]

class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['description', 'hourly_rate', 'daily_rate']
    ordering = ['description']

class PodAdmin(admin.ModelAdmin):
    list_display = ['description']
    ordering = ['description']

admin.site.register(VehicleType, VehicleTypeAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Pod, PodAdmin)