from django.conf.urls import url

from . import views


app_name = 'carshare'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'contact-us/$', views.contact_us, name='contact_us'),
    url(r'find-a-car/$', views.find_a_car, name='find_a_car'),
    # url(r'bookings/$', views.bookings, name='bookings'),
    url(r'bookings/new/vehicle-(?P<vehicle_name>[a-zA-Z]+)/$', views.new_booking, name='new_booking'),
    url(r'bookings/(?P<booking_id>[0-9]+)/$', views.booking_detail, name='booking_detail'),
]