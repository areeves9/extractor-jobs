from django.views.generic import ListView
from django.views.generic.detail import DetailView
from jobs.models import Job

from django.shortcuts import render, get_object_or_404


class JobList(ListView):
    """
    Get all Job instances from the database.
    """
    model = Job
    context_object_name = 'job_list'


class JobDetailView(DetailView):
    """
    Get detail for single job instance.
    """
    model = Job
    context_object_name = 'job'
