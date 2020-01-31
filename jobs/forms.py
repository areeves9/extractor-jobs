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
