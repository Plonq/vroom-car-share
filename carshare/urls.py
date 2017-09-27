from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'contact-us/$', views.contact_us, name='contact_us'),
    url(r'findacar/$', views.findacar, name='findacar'),
]