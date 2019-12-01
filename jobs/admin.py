from django.contrib import admin
from jobs.models import Job

# Register your models here.


class JobModelAdmin(admin.ModelAdmin):
    list_display = ["headline", "post_date"]
    list_filter = ["post_date"]
    search_fields = []

    class Meta:
        model = Job


admin.site.register(Job, JobModelAdmin)
