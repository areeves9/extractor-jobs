from django.contrib.messages.views import SuccessMessageMixin

import json
from django.http import JsonResponse
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from jobs.models import Job
from jobs.forms import JobForm


class JobCreate(CreateView):
    form_class = JobForm
    template_name = 'jobs/job_form.html'


class JobUpdate(SuccessMessageMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_message = 'Job posting sucessfuly updated.'


class JobDelete(DeleteView):
    model = Job
    success_url = reverse_lazy('jobs:job_list')


class JobList(ListView):
    """
    Get all Job instances from the database.
    """
    model = Job
    context_object_name = 'job_list'
    paginate_by = 10


class JobDetailView(DetailView):
    """
    Get detail for single job instance.
    """
    model = Job
    context_object_name = 'job'


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


# class JobLike(View):
#     def get(self, request, *args, **kwargs):
#         slug = self.request.kwargs("slug")
#         action = self.request.kwargs("action")
#         print(action)
#         if slug and action:
#             try:
#                 if action == 'like':
#                     job.likes.add(request.user)
#                 else:
#                     job.likes.remove(request.user)
#                 return HttpResponse('Hello, World!')
#             except:
#                 pass
#         return HttpResponse('Hello, World!')

