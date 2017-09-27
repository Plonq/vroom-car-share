from django.contrib import admin

from .models import Vehicle, Pod, VehicleType


admin.site.register(VehicleType)
admin.site.register(Vehicle)
admin.site.register(Pod)