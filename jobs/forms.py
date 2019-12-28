from dal import autocomplete

from django import forms
from cities_light.models import Country
from jobs.models import Job


class JobForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=autocomplete.ModelSelect2(url='country-autocomplete')
    )

    class Meta:
        model = Job
        exclude = ('slug',)
