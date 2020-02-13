from django.contrib import admin
from jobs.models import Job

# Register your models here.


class JobModelAdmin(admin.ModelAdmin):
    list_display = (
        "job_title",
        "headline",
        "slug",
        "location",
        "post_date",
        "employment_type",
        "low_salary",
        "high_salary",
        "link",
    )
    list_filter = ("post_date",)
    search_fields = ["location"]

    class Meta:
        model = Job


admin.site.register(Job, JobModelAdmin)
