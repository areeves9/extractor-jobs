# from django.conf.urls import url
from django.urls import include, re_path

from django.contrib.auth.decorators import login_required

from utils.autocomplete import CityAutocomplete, RegionAutocomplete, CountryAutocomplete

from accounts.views import RegistrationView, UserDetailView, UserUpdateView, UserListView, UserProfileView, ExperienceView, ExperienceUpdateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(
        r'^city-autocomplete/$',
        CityAutocomplete.as_view(),
        name='city-autocomplete',
    ),
    re_path(
        r'^region-autocomplete/$',
        RegionAutocomplete.as_view(),
        name='region-autocomplete',
    ),
    re_path(
        r'^country-autocomplete/$',
        CountryAutocomplete.as_view(),
        name='country-autocomplete',
    ),
    re_path(r'^register/$', RegistrationView.as_view(), name='register'),
    re_path(r'^profile/$', login_required(UserProfileView.as_view()), name='profile'),
    re_path(r'^profile/(?P<slug>[-\w]+)/$', login_required(UserDetailView.as_view()), name='profile_detail'),
    re_path(r'^profile/(?P<slug>[-\w]+)/update/$', login_required(UserUpdateView.as_view()), name='profile_update'),
    re_path(r'^user/list/$', login_required(UserListView.as_view()), name='user_list'),
    re_path(r'^login/$', auth_views.LoginView.as_view(), name="login"),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name="logout"),
    re_path(r'^experience/add/$', login_required(ExperienceView.as_view()), name="experience_add"),
    re_path(r'^experience/(?P<pk>\d+)/update/$', login_required(ExperienceUpdateView.as_view()), name="experience_update"),
]
