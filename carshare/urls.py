from django.conf.urls import url

from . import views


app_name = 'carshare'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'contact-us/$', views.contact_us, name='contact_us'),
    url(r'find-a-car/$', views.find_a_car, name='find_a_car'),
    url(r'bookings/new/(?P<vehicle_id>[0-9]+)/$', views.booking_timeline, name='booking_create'),
    url(r'bookings/new/(?P<vehicle_id>[0-9]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/$', views.booking_timeline, name='booking_create_date'),
    url(r'bookings/new/(?P<vehicle_id>[0-9]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<hour>[0-9]{1,2})/$', views.booking_create, name='booking_create_final'),
    url(r'bookings/(?P<booking_id>[0-9]+)/$', views.booking_detail, name='booking_detail'),
    url(r'bookings/(?P<booking_id>[0-9]+)/extend/$', views.booking_extend, name='booking_extend'),
    url(r'bookings/$', views.my_bookings, name='my_bookings'),
]
