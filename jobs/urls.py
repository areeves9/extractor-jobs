from django.conf.urls import url
from jobs.views import JobList, JobDetailView, JobCreate


urlpatterns = [
    url(r'^$', JobList.as_view(), name='job-list'),
    url(r'^create/$', JobCreate.as_view(), name='job-create'),
    url(r'^(?P<slug>[-\w]+)/$', JobDetailView.as_view(), name="job-detail"),
]
