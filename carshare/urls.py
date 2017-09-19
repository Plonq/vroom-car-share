from django.conf.urls import url

from . import views
from registration import registration_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', registration_views.register, name='register')
]