from django.conf.urls import url
from jobs.views import JobList, JobDetailView, JobCreate, JobUpdate, JobDelete

urlpatterns = [
    url(r'^$', JobList.as_view(), name='job_list'),
    url(r'^create/$', JobCreate.as_view(), name='job_create'),
    url(r'^(?P<slug>[-\w]+)/update/$', JobUpdate.as_view(), name='job_update'),
    url(r'^(?P<slug>[-\w]+)/delete/$', JobDelete.as_view(), name='job_delete'),
    url(r'^(?P<slug>[-\w]+)/$', JobDetailView.as_view(), name="job_detail"),
]
