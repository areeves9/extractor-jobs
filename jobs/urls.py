from django.conf.urls import url
from jobs.autocomplete import CityAutocomplete, RegionAutocomplete, CountryAutocomplete

from jobs.views import JobList, JobDetailView, JobCreate, JobUpdate, JobDelete

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
    url(r'^$', JobList.as_view(), name='job_list'),
    url(r'^create/$', JobCreate.as_view(), name='job_create'),
    url(r'^(?P<slug>[-\w]+)/update/$', JobUpdate.as_view(), name='job_update'),
    url(r'^(?P<slug>[-\w]+)/delete/$', JobDelete.as_view(), name='job_delete'),
    url(r'^(?P<slug>[-\w]+)/$', JobDetailView.as_view(), name="job_detail"),
]
