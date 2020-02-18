from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin


from smtplib import SMTPException

from django.template.loader import render_to_string

import json
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render


from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from formtools.wizard.views import SessionWizardView

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
from jobs.forms import JobShareForm, JobForm


class JobWizard(SuccessMessageMixin, SessionWizardView):
    success_message = 'Job posting sucessfuly created.'
    
    def done(self, form_list, **kwargs):
        form_dict = self.get_all_cleaned_data()
        print(form_dict)
        instance = Job.objects.create(
            **form_dict,
            user=self.request.user,
        )
        print(instance)

        return render(self.request, 'formtools/wizard/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })


class JobCreate(SuccessMessageMixin, UserPassesTestMixin, CreateView):
    """
    Create a job instance.
    """
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_message = 'Job posting sucessfuly created.'
    permission_denied_message = 'DENIED!'

    def test_func(self):
        return self.request.user.is_business

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        body = json.loads(request.body)
        email_recipient = body['email_recipient']

        if email_recipient:
            try:
                subject = self.object.headline
                from_mail = request.user.email
                job_url = request.build_absolute_uri(self.object.get_absolute_url())
                html_message = render_to_string(
                    'jobs/job_email.html',
                    context={
                        'job': self.object,
                        'user': request.user,
                        'domain': request.META['HTTP_HOST']
                    }
                )
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





class JobUpdate(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    """
    Update a job instance.
    """
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_message = 'Job posting sucessfuly updated.'

    def test_func(self):
        return self.request.user.job_set.filter(pk=self.get_object().pk).exists()


class JobDelete(SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a job instance.
    """
    model = Job
    success_url = reverse_lazy('jobs:job_list')
    success_message = 'Job posting sucessfuly deleted.'

    def test_func(self):
        return self.request.user.job_set.filter(pk=self.get_object().pk).exists()


@login_required
@require_POST
def job_like(request):
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