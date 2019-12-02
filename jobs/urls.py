from django.conf.urls import url
from jobs.views import JobList, JobDetailView, JobCreate, JobUpdate, JobDelete


urlpatterns = [
    url(r'^$', JobList.as_view(), name='job-list'),
    url(r'^create/$', JobCreate.as_view(), name='job-create'),
    url(r'^(?P<slug>[-\w]+)/update$', JobUpdate.as_view(), name='job-update'),
    url(r'^(?P<slug>[-\w]+)/delete/$', JobDelete.as_view(), name='job-delete'),
    url(r'^(?P<slug>[-\w]+)/$', JobDetailView.as_view(), name="job-detail"),
]
