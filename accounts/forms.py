from django import forms
from dal import autocomplete
from cities_light.models import City

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from accounts.models import SiteUser, Experience, Skill


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = SiteUser
        fields = ('email', 'display_name', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url='jobs:city-autocomplete')
    )

    class Meta:
        model = SiteUser
        labels = {
            'is_available': 'Looking for work?',
        }
        exclude = (
            'email',
            'password',
            'last_login',
            'height_field',
            'width_field',
            'is_admin',
            'is_staff',
            'is_business',
            'is_active',
            'slug',
        )


class ExperienceForm(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url='jobs:city-autocomplete')
    )

    class Meta:
        model = Experience
        fields = (
            'company',
            'location',
            'title',
            'is_present_employeer',
            'start_month',
            'start_year',
            'end_month',
            'end_year',
            'description',
        )
        exclude = (
            'date_created',
            'date_updated',
            'user',
        )


class SkillForm(forms.ModelForm):

    class Meta:
        model = Skill
        exclude = (
            'user',
        )
        help_texts = {
            'tags': 'Separate tags with commas.',
        }
        labels = {'tags': ''}


class RegisterForm(forms.ModelForm):
    """
    For Django Admin user creation.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = SiteUser
        fields = ('email', 'display_name',)

        def clean_email(self):
            email = self.cleaned_data.get('email')
            qs1 = SiteUser.objects.filter(email=email)
            if qs1.exists:
                raise forms.ValidationError("email is taken")
            return email

        def cleaned_password2(self):
            #  Make sure  passwords match
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords do not match")
            return password2


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = SiteUser
        fields = ('email', 'display_name', 'password1', 'password2',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = SiteUser
        fields = ('email', 'password',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class BusinessRequestForm(forms.Form):
    business_name = forms.CharField(
        label='Business name.',
        max_length=255,
    )
    location = forms.CharField(
        label='Business location.',
        max_length=255,
    )
    address = forms.CharField(
        label='Business mailing address.',
        max_length=255,
    )
    license_id = forms.CharField(
        label='Business license issued by state regulatory agency.',
        max_length=255,
    )
    message = forms.CharField(
        label='Additional information.',
        widget=forms.Textarea,
    )
    
    # def send_mail(self):
    #     subject = 'Request for business account from {{ self.request.user }}'
    #     message = render_to_string('registration/business_request_email.html', {
    #         'user': self.request.user,
    #         'business_name': self.form.cleaned_data['business_name'],
    #         'location': self.form.cleaned_data['location'],
    #         'address': self.form.cleaned_data['address'],
    #         'license_id': self.form.cleaned_data['license_id'],

    #     })
    #     email = EmailMessage(subject, message, to=['areeves9@icloud.com', ])
    #     email.send()
