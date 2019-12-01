from django.views.generic import ListView 
from jobs.models import Job


class JobList(ListView):
    """
    Get all Job instances from the database.
    """
    model = Job
    context_object_name = 'job_list'


