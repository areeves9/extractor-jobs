from django.urls import re_path
from utils.autocomplete import CityAutocomplete

from jobs.views import JobList, JobDetailView, JobCreate, JobUpdate, JobDelete

urlpatterns = [
    re_path(
        r'^city-autocomplete/$',
        CityAutocomplete.as_view(),
        name='city-autocomplete',
    ),
    re_path(r'^$', JobList.as_view(), name='job_list'),
    re_path(r'^create/$', JobCreate.as_view(), name='job_create'),
    re_path(r'^(?P<slug>[-\w]+)/update/$', JobUpdate.as_view(), name='job_update'),
    re_path(r'^(?P<slug>[-\w]+)/delete/$', JobDelete.as_view(), name='job_delete'),
    re_path(r'^(?P<slug>[-\w]+)/$', JobDetailView.as_view(), name="job_detail"),
]
