from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from utils.autocomplete import CityAutocomplete, RegionAutocomplete, CountryAutocomplete

from accounts.views import RegistrationView, UserDetailView, UserUpdateView, UserListView, UserProfileView
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(
        r'^city-autocomplete/$',
        CityAutocomplete.as_view(),
        name='city-autocomplete',
    ),
    url(
        r'^region-autocomplete/$',
        RegionAutocomplete.as_view(),
        name='region-autocomplete',
    ),
    url(
        r'^country-autocomplete/$',
        CountryAutocomplete.as_view(),
        name='country-autocomplete',
    ),
    url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^profile/$', login_required(UserProfileView.as_view()), name='profile'),
    url(r'^profile/(?P<slug>[-\w]+)/$', login_required(UserDetailView.as_view()), name='profile_detail'),
    url(r'^profile/(?P<slug>[-\w]+)/update/$', login_required(UserUpdateView.as_view()), name='profile_update'),
    url(r'^user/list/$', login_required(UserListView.as_view()), name='user_list'),
    url(r'^login/$', auth_views.LoginView.as_view(), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name="logout"),
]
