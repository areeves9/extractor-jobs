from django.conf.urls import url

from jobs import views

urlpatterns = [
    url(r'^job/$', views.job, name="job"),
]
