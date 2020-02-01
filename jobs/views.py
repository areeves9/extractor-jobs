from django.contrib.messages.views import SuccessMessageMixin

from smtplib import SMTPException

from django.template.loader import render_to_string

import json
from django.http import JsonResponse
from django.urls import reverse_lazy

from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from jobs.models import Job
from jobs.forms import JobForm, JobShareForm


class JobDetail(DetailView):
    """
    Get detail for single job instance.
    """
    model = Job
    context_object_name = 'job'


class JobShare(FormMixin, DetailView):
    model = Job
    form_class = JobShareForm
    template_name = 'jobs/job_share_form.html'
    context_object_name = 'job'
    success_message = 'Job posting `sucessfuly` created.'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        body = json.loads(request.body)
        email_recipient = body['email_recipient']

        if email_recipient:
            try:
                subject = self.object.headline
                from_mail = request.user.email
                job_url = request.build_absolute_uri(self.object.get_absolute_url())
                html_message = render_to_string('jobs/job_email.html', context={'job': self.object})
                text_content = 'Read "{}" at {}.'.format(self.object.headline, job_url)
                msg = EmailMultiAlternatives(
                    subject, text_content, from_mail, [email_recipient]
                )
                msg.attach_alternative(html_message, "text/html")
                msg.mixed_subtype = 'related'
                msg.send()
            except SMTPException as e:
                logging.error('SMTPException: %s' % e)

        else:
            return JsonResponse({'status': 'error'})

        return JsonResponse({'status': 'ok'})


class JobList(ListView):
    """
    Get all Job instances from the database.
    """
    model = Job
    context_object_name = 'job_list'
    paginate_by = 10


class JobCreate(SuccessMessageMixin, CreateView):
    """
    Create a job instance.
    """
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_message = 'Job posting sucessfuly created.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class JobUpdate(SuccessMessageMixin, UpdateView):
    """
    Update a job instance.
    """
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_message = 'Job posting sucessfuly updated.'


class JobDelete(SuccessMessageMixin, DeleteView):
    """
    Delete a job instance.
    """
    model = Job
    success_url = reverse_lazy('jobs:job_list')
    success_message = 'Job posting sucessfuly deleted.'


@login_required
@require_POST
def job_like(request):
    # slug = request.POST.get('slug')
    # action = request.POST.get('action')
    body = json.loads(request.body)
    slug = body['slug']
    action = body['action']
    print(slug)
    if slug and action:
        try:
            job = Job.objects.get(slug=slug)
            if action == 'like':
                print(action)
                job.likes.add(request.user)
            else:
                job.likes.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})
