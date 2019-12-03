from django.conf.urls import url
from accounts.views import RegistrationView
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name="login"),
]
