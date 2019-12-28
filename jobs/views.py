from dal import autocomplete
from cities_light.models import Country

from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from jobs.models import Job
from jobs.forms import JobForm


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Country.objects.none()

        qs = Country.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class JobCreate(CreateView):
    form_class = JobForm
    success_url = reverse_lazy('jobs:job_list')
    template_name = 'jobs/job_form.html'
    # model = Job
    # fields = [
    #     'description',
    #     'expiration_date',
    #     'employment_type',
    #     'education',
    #     'headline',
    #     'country',
    #     'city',
    #     'state',
    #     'salary',
    #     'salary_frequency',
    #     'benefits',
    #     'link',
    #     'job_title',
    # ]


class JobUpdate(UpdateView):
    model = Job
    fields = [
        'description',
        'expiration_date',
        'employment_type',
        'education',
        'headline',
        'country',
        'city',
        'state',
        'salary',
        'salary_frequency',
        'benefits',
        'link'
        'job_title',
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
