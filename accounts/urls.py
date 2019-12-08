from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from accounts.views import RegistrationView, UserDetailView
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^profile/$', login_required(UserDetailView.as_view()), name='profile'),
    url(r'^login/$', auth_views.LoginView.as_view(), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name="logout"),
]
