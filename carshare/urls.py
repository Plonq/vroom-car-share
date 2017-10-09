from django.conf.urls import url

from . import views


app_name = 'carshare'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'contact-us/$', views.contact_us, name='contact_us'),
    url(r'find-a-car/$', views.find_a_car, name='find_a_car'),
    url(r'bookings/new/(?P<vehicle_id>[0-9]+)/$', views.booking_create, name='booking_create'),
    url(r'bookings/(?P<booking_id>[0-9]+)/$', views.booking_detail, name='booking_detail'),
    url(r'bookings/$', views.booking_index, name='booking_index'),
]
