from dal import autocomplete

from django import forms
from cities_light.models import City
from jobs.models import Job


class JobForm(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url='jobs:city-autocomplete')
    )

    class Meta:
        model = Job
        exclude = ('slug','likes',)
