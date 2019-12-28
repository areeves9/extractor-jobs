from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from jobs.models import Job
from jobs.forms import JobForm


class JobCreate(CreateView):
    form_class = JobForm
    template_name = 'jobs/job_form.html'


class JobUpdate(UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'


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
