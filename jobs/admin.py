from django.contrib import admin
from jobs.models import Job

# Register your models here.


class JobModelAdmin(admin.ModelAdmin):
    list_display = ("job_title", "headline", "slug", "city", "state", "post_date", "employment_type", "salary", "link")
    list_filter = ("post_date", "state")
    search_fields = ["state"]

    class Meta:
        model = Job


admin.site.register(Job, JobModelAdmin)
