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
    US_STATES_CHOICES = (('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name']  # email and password automatically required

    # objects = SiteUserManager()

    bio = models.TextField(blank=True, null=True)
    display_name = models.CharField(
        max_length=255,
        unique=True
    )
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
        choices=US_STATES_CHOICES,
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

    def display_name(self):
        return self.display_name

    def has_perm(self, perm, obj=None):
        #  does user have permissions?
        return True

    def has_module_perms(self, app_label):
        return True
