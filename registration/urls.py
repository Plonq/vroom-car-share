from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
]
