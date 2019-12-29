from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from cities_light.models import City, Country, Region

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
# display names only have alphanumeric and underscores
alphanumeric_underscores = RegexValidator(r'^[a-zA-Z0-9_]+$', 'Only alphanumeric and underscores')


def upload_location(instance, filename):
    return "%s/%s" % (instance.display_name, filename)


class SiteUserManager(BaseUserManager):
    def create_user(self, email, display_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            display_name=display_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, display_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            display_name=display_name,
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
    EDUCATION_CHOICES = (
        ('HS', 'High School/GRE'),
        ('AS', 'Associate\'s'),
        ('BA/BS', 'Bachelor\'s'),
        ('MA/MS', 'Master\'s'),
        ('PHD', 'Doctorate'),
    )
    bio = models.TextField(blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    display_name = models.CharField(
        blank=False,
        null=True,
        max_length=255,
        unique=True,
        validators=[alphanumeric_underscores]
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    education = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        choices=EDUCATION_CHOICES,
    )
    headline = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name']  # email and password automatically required

    objects = SiteUserManager()

    first_name = models.CharField(
        blank=True,
        null=True,
        max_length=255
    )
    last_name = models.CharField(
        blank=True,
        null=True,
        max_length=255,
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
    city = models.ForeignKey(
        City,
        verbose_name='city',
        blank=True,
        null=True,
    )
    country = models.ForeignKey(
        Country,
        verbose_name='country',
        blank=True,
        null=True,

    )
    state = models.ForeignKey(
        Region,
        verbose_name='region',
        blank=True,
        null=True,
    )
    phone_number = PhoneNumberField(blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        """
        Overirde the model save method to set slug field to username
        """
        if not self.slug:
            self.slug = slugify(self.display_name)
        super(SiteUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("accounts:profile_detail", kwargs={"slug": self.slug})

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