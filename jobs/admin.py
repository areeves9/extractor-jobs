from django.contrib import admin
from jobs.models import Job

# Register your models here.


class JobModelAdmin(admin.ModelAdmin):
    list_display = ("headline", "city", "state", "post_date", "job_type", "salary",)
    list_filter = ("post_date",)
    search_fields = ["state"]

    class Meta:
        model = Job


admin.site.register(Job, JobModelAdmin)
