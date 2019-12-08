from django.conf.urls import url
from accounts.views import RegistrationView
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^login/$', auth_views.LoginView.as_view(), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name="logout"),
]
