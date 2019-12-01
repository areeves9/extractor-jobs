from django.db import models
from django.core.urlresolvers import reverse

from django.db.models.signals import pre_save

from django.utils.text import slugify

# Create your models here.


class Job(models.Model):
    """
    A job with information found externally. Can be
    created by an Admin or a SiteUser with Emoployer
    account type.
    """
    EDUCATION_CHOICES = (
        ('HS', 'High School/GRE'),
        ('BA/BS', 'Bachelor of Art and Science'),
        ('MA/MS', 'Master of Art and Science'),
        ('PHD', 'Doctor of Philosophy')
    )
    JOB_CATEGORY_CHOICES = (
        ('TECHNICIAN', 'Technician'),
        ('CHEMIST', 'Chemist'),
    )
    JOB_TYPE_CHOICES = (
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('1099', 'Contract'),
    )
    description = models.TextField()
    slug = models.SlugField(unique=True)
    expiry = models.DateField()
    post_date = models.DateField(auto_now_add=True)
    job_category = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        choices=JOB_CATEGORY_CHOICES,
    )
    job_type = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        choices=JOB_TYPE_CHOICES,
    )
    education = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        choices=EDUCATION_CHOICES,
    )
    experience = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    headline = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    skills = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    city = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    state = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    salary = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    benefits = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    link = models.URLField(
        blank=True,
        null=True,
        max_length=255,
    )

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse("jobs:job-detail", kwargs={"slug": self.slug})

# if instance doesn't have slug
# pass instance to create_slug
# slug is created from instance.headline
# then check db if job already has the slug
# if there is a job with same slug, then
# create new_slug by adding instance.id  
# and pass with instance to create
# slug.  Then return slug.


def create_slug(instance, new_slug=None):
    slug = slugify(instance.headline)
    if new_slug is not None:
        slug = new_slug
    qs = Job.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_job_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_job_reciever, sender=Job)
