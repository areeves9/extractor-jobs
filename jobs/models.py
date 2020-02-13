import datetime
from jobsite import settings
from django.db import models
from django.urls import reverse

from django.db.models.signals import pre_save

from cities_light.models import City
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
        ('AS', 'Associate\'s'),
        ('BA/BS', 'Bachelor\'s'),
        ('MA/MS', 'Master\'s'),
        ('PHD', 'Doctorate')
    )

    EMPLOYMENT_TYPE_CHOICES = (
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Contract', 'Contract'),
    )
    SALARY_FREQUENCY_CHOICES = (
        ('HR', 'Per-Hour'),
        ('DAY', 'Daily'),
        ('WEEK', 'Weekly'),
        ('MONTH', 'Monthly'),
        ('YEAR', 'Yearly'),
    )
    description = models.TextField(
         help_text="Describe the position and the working conditions."
    )
    expiration_date = models.DateField(
        blank=True,
        null=True,
        help_text="Please use the following format: <em>YYYY-MM-DD</em>."
    )
    employment_type = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        choices=EMPLOYMENT_TYPE_CHOICES,
    )
    education = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        choices=EDUCATION_CHOICES,
    )
    headline = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        help_text="A concise high-level overview of the job."
    )
    post_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        )
    location = models.ForeignKey(
        City,
        verbose_name='location',
        on_delete=models.PROTECT,
    )
    low_salary = models.DecimalField(
        blank=True,
        null=True,
        max_digits=15,
        decimal_places=2,
        help_text="Two decimal places. Ex. 65,200.23"

    )
    low_salary_frequency = models.CharField(
        blank=True,
        null=True,
        max_length=225,
        choices=SALARY_FREQUENCY_CHOICES,
    )
    high_salary = models.DecimalField(
        blank=True,
        null=True,
        max_digits=15,
        decimal_places=2,
        help_text="Two decimal places. Ex. 65,200.23"

    )
    high_salary_frequency = models.CharField(
        blank=True,
        null=True,
        max_length=225,
        choices=SALARY_FREQUENCY_CHOICES,
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
    job_title = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='jobs_liked',
        blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1
    )

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse("jobs:job_detail", kwargs={"slug": self.slug})

    def get_post_date_days(self):
        post_date = self.post_date
        current_date = datetime.datetime.now().date()
        delta = current_date - post_date
        return delta.days

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
