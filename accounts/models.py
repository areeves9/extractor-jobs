from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator


# Create your models here.
# display names only have alphanumeric and underscores
alphanumeric_underscores = RegexValidator(r'^[a-zA-Z0-9_]+$', 'Only alphanumeric and underscores')


def upload_location(instance, filename):
    return "%s/%s" % (instance.display_name, filename)


class SiteUserManager(BaseUserManager):
    def create_user(self, email, display_name, account_type, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            display_name=display_name,
            account_type=account_type,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, display_name, account_type, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            display_name=display_name,
            account_type=account_type,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class SiteUser(AbstractBaseUser):
    """
    This is a custom user subclassing the Django
    AbstrctBaseUser. From this class, the Employeer
    class is subclassed. Employeers have the ability
    to create, edit, delete job posts.
    """
    ACCOUNT_TYPE_CHOICES = (
        ('CANDIDATE', 'Candidate'),
        ('EMPLOYER', 'Employer'),
    )
    US_STATES_CHOICES = (('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )

    display_name = models.CharField(
        blank=False,
        null=True,
        max_length=255,
        unique=True,
        validators=[alphanumeric_underscores]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name', 'account_type']  # email and password automatically required

    objects = SiteUserManager()

    bio = models.TextField(blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    first_name = models.CharField(
        blank=True,
        null=True,
        max_length=255
    )
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field",
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    last_name = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    # when the user joined the site
    location_city = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        unique=False,
    )
    location_state = models.CharField(
        blank=True,
        null=True,
        choices=US_STATES_CHOICES,
        max_length=255,
        unique=False,
    )
    phone_number = PhoneNumberField(blank=True)

    # password field is builtin
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    account_type = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        choices=ACCOUNT_TYPE_CHOICES,
    )

    def __str__(self):
        return self.email

    def get_full_name(self):
        return F"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def get_display_name(self):
        return self.display_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class CandidateProfile(models.Model):
    """
    Extends the SiteUser model by adding additional fields.
    There is a CandidateProfile and EmployerProfile. The
    CandidateProfile will contain fields specific to extraction.
    """
    EDUCATION_CHOICES = (
        ('HS', 'High School/GRE'),
        ('BA/BS', 'Bachelor of Art and Science'),
        ('MA/MS', 'Master of Art and Science'),
        ('PHD', 'Doctor of Philosophy')
    )
    SPECIALITY_CHOICES = (
        ('SYNTHESIS', 'Cannabinoid Synthesis'),
        ('EXTRACTION', 'Cannabinoid/Terpene Extraction'),
        ('POSTPROCESS', 'Winterization/Solvent Recovery'),
        ('DISTILLATION', 'Cannabinoid Distillation'),
        ('ANALYTICS', 'Cannabinoid Analytics'),
        ('ISOLATIONS', 'Flash Chromatography/Crystallization'),
    )
    TITLE_CHOICES = (
        ('TECHNICIAN', 'Technician'),
        ('CHEMIST', 'Chemist'),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    education = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        choices=EDUCATION_CHOICES,
    )
    speciality = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        choices=SPECIALITY_CHOICES,
    )
    field_of_study = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    headline = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    title = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        choices=TITLE_CHOICES,
    )