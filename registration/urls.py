from django.conf.urls import url, include

from . import registration_views

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^profile$', registration_views.profile),
    url(r'^register$', registration_views.register)

]