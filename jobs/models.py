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
    US_STATES_CHOICES = (('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))
    EDUCATION_CHOICES = (
        ('HS', 'High School/GRE'),
        ('AS', 'Associate\'s'),
        ('BA/BS', 'Bachelor\'s'),
        ('MA/MS', 'Master\'s'),
        ('PHD', 'Doctorate')
    )

    EMPLOYMENT_TYPE_CHOICES = (
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('1099', 'Contract'),
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
    slug = models.SlugField(unique=True)
    city = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    state = models.CharField(
        blank=True,
        null=True,
        choices=US_STATES_CHOICES,
        max_length=255,
        unique=False,
    )
    salary = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    salary_frequency = models.CharField(
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

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse("jobs:job_detail", kwargs={"slug": self.slug})

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
