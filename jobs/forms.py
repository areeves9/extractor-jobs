from dal import autocomplete

from django import forms
from cities_light.models import City, Region, Country
from jobs.models import Job


class JobForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url='jobs:city-autocomplete')
    )
    state = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        widget=autocomplete.ModelSelect2(url='jobs:region-autocomplete')
    )
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=autocomplete.ModelSelect2(url='jobs:country-autocomplete')
    )

    class Meta:
        model = Job
        exclude = ('slug',)
