from dal import autocomplete

from django import forms

from cities_light.models import City
from jobs.models import Job


class JobShareForm(forms.Form):
    send_to = forms.EmailField()
    subject = forms.CharField(max_length=90)

    class Meta:
        fields = ["send_to", "subject", "message"]


class JobForm(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url='jobs:city-autocomplete')
    )

    class Meta:
        model = Job
        exclude = ('slug', 'likes', 'user')


class JobForm1(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url='jobs:city-autocomplete')
    )

    class Meta:
        model = Job
        fields = ('job_title', 'headline', 'location', 'description',)


class JobForm2(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('low_salary', 'low_salary_frequency', 'high_salary', 'high_salary_frequency',)


class JobForm3(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('link', 'expiration_date', 'employment_type', 'education', 'benefits',)