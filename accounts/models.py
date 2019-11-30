from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class SiteUser(AbstractBaseUser):
    """
    This is a custom user subclassing the Django
    AbstrctBaseUser. From this class, the Employeer
    class is subclassed. Employeers have the ability
    to create, edit, delete job posts.
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    # username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # email and password automatically required

    # objects = SiteUserManager()

    bio = models.TextField(blank=True, null=True) 
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
    # when the user joined the site
    join_date = models.DateField(auto_now_add=True)
    location_city = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        unique=False,
    )
    location_state = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        unique=False,
    )
    phone_number = PhoneNumberField(blank=True)

    # password field is builtin
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return F"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def get_location(self):
        return self.location

    def has_perm(self, perm, obj=None):
        #  does user have permissions?
        return True

    def has_module_perms(self, app_label):
        return True