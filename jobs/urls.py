from django.conf.urls import url
from jobs.views import JobList


urlpatterns = [
    url(r'^$', JobList.as_view(), name='job-list'),
    url(r'^(?P<id>\d+)/$', JobDetailView.as_view(), name="job-detail"),
]
