from django.conf.urls import url
from jobs.views import JobList, JobDetailView


urlpatterns = [
    url(r'^$', JobList.as_view(), name='job-list'),
    url(r'^(?P<slug>\w+)/$', JobDetailView.as_view(), name="job-detail"),
]
