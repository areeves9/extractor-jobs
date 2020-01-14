import datetime
import os
from io import BytesIO

from django.core.files import File

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image, ExifTags
from cities_light.models import City

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator

from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager

from imagekit.models import ImageSpecField
from imagekit.processors import Transpose






# Create your models here.
# display names only have alphanumeric and underscores
alphanumeric_underscores = RegexValidator(r'^[a-zA-Z0-9_]+$', 'Only alphanumeric and underscores')

# Create your models here.

# https://medium.com/@giovanni_cortes/rotate-image-in-django-when-saved-in-a-model-8fd98aac8f2a
# rotate saved image to imagefield with django signals post save
# def rotate_image(filepath):
#   try:
#     print(filepath)
#     image = Image.open(filepath)
#     print(image.name)
#     for orientation in ExifTags.TAGS.keys():
#       if ExifTags.TAGS[orientation] == 'Orientation':
#             break
#     exif = dict(image._getexif().items())

#     if exif[orientation] == 3:
#         image = image.rotate(180, expand=True)
#     elif exif[orientation] == 6:
#         image = image.rotate(270, expand=True)
#     elif exif[orientation] == 8:
#         image = image.rotate(90, expand=True)
#     image.save(filepath, overwrite=True)
#     image.close()
#   except (AttributeError, KeyError, IndexError):
    # pass

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
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
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
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)
    location = models.ForeignKey(
        City,
        verbose_name='location',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
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
        if self.image:
            pilImage = Image.open(BytesIO(self.image.read()))
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(pilImage._getexif().items())

            if exif[orientation] == 3:
                pilImage = pilImage.rotate(180, expand=True)
            elif exif[orientation] == 6:
                pilImage = pilImage.rotate(270, expand=True)
            elif exif[orientation] == 8:
                pilImage = pilImage.rotate(90, expand=True)

            output = BytesIO()
            pilImage.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.image = File(output, self.image.name)

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

# @receiver(post_save, sender=SiteUser)
# def update_image(sender, instance, **kwargs):
#     if instance.image:
#         BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         fullpath = BASE_DIR + instance.image.url
#         rotate_image(fullpath)

class Skill(models.Model):
    """
    Each SiteUser instance has a 1-to-1 relationship with Skill,
    with SKill having tags attribute. This way the user can 
    add many skill tags with a single skill instance.
    """
    user = models.OneToOneField(
        SiteUser,
        related_name='skill',
        on_delete=models.CASCADE,
    )
    tags = TaggableManager(blank=True)

    def get_absolute_url(self):
        return reverse("accounts:skill_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.tags)


@receiver(post_save, sender=SiteUser)
def create_user_skill(sender, instance, created, **kwargs):
    if created:
        Skill.objects.create(user=instance)


@receiver(post_save, sender=SiteUser)
def save_user_profile(sender, instance, **kwargs):
    instance.skill.save()


class Experience(models.Model):
    """
    Foreign key relationship to SiteUser. Describes
    previous work experiences associated with SiteUser
    instance.
    """
    MONTH_CHOICES = (
        ('Janurary', 'Janurary'),
        ('Feburary', 'Feburary'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    )

    def get_year_choices():
        YEAR_CHOICES = []

        for r in range(1980, (datetime.datetime.now().year+1)):
            YEAR_CHOICES.append((r,r))
        return YEAR_CHOICES

    company = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey(
        City,
        verbose_name='city',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    start_month = models.CharField(
        choices=MONTH_CHOICES,
        max_length=20,
        blank=False,
        null=False,
    )
    end_month = models.CharField(
        choices=MONTH_CHOICES,
        max_length=20,
        blank=False,
        null=False,
    )
    start_year = models.IntegerField(
        choices=get_year_choices(),
    )
    end_year = models.IntegerField(
        choices=get_year_choices(),
    )
    user = models.ForeignKey(
        SiteUser,
        verbose_name='user',
        on_delete=models.PROTECT
    )

    is_employeer = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("accounts:experience_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.company

