from django.urls import re_path
from utils.autocomplete import CityAutocomplete
from django.contrib.auth.decorators import login_required

from jobs import views


from jobs.views import (
    JobList,
    JobCreate,
    JobUpdate,
    JobDelete,
    JobDetail,
    JobShare
)
urlpatterns = [
    re_path(
        r'^city-autocomplete/$',
        CityAutocomplete.as_view(),
        name='city-autocomplete',
    ),
    re_path(r'^$', JobList.as_view(), name='job_list'),
    re_path(r'^like/$', login_required(views.job_like), name='job_like'),
    re_path(r'^create/$', login_required(JobCreate.as_view()), name='job_create'),
    re_path(r'^(?P<slug>[-\w]+)/$', login_required(JobDetail.as_view()), name="job_detail"),
    re_path(r'^(?P<slug>[-\w]+)/delete/$', login_required(JobDelete.as_view()), name='job_delete'),
    re_path(r'^(?P<slug>[-\w]+)/update/$', login_required(JobUpdate.as_view()), name='job_update'),
    re_path(r'^(?P<slug>[-\w]+)/share/$', login_required(JobShare.as_view()), name='job_share'),
]
