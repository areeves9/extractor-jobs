from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from jobs.models import Job


class JobCreate(CreateView):
    model = Job
    fields = [
        'description',
        'expiry',
        'job_category',
        'job_type',
        'education',
        'experience',
        'headline',
        'city',
        'state',
        'salary',
        'benefits',
        'link'
    ]


class JobUpdate(UpdateView):
    model = Job
    fields = [
        'description',
        'expiry',
        'job_category',
        'job_type',
        'education',
        'experience',
        'headline',
        'city',
        'state',
        'salary',
        'benefits',
        'link'
    ]


class JobDelete(DeleteView):
    model = Job
    success_url = reverse_lazy('jobs:job_list')


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
