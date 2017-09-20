from django.conf.urls import url, include
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView

from . import forms
from . import views


urlpatterns = [
    # Override django auth templates with our own
    url(r'^logout/$', LogoutView.as_view(template_name='accounts/logged_out.html')),
    url(r'^password_change/$', PasswordChangeView.as_view(template_name='accounts/password_change_form.html', form_class=forms.PasswordChangeForm)),
    url(r'^password_change/done/$', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html')),
    # Fall back on defaults for everything else
    url(r'^', include('django.contrib.auth.urls')),
    # Other accounts-related pages not included in django auth
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
]
