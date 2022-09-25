from django import forms

from mainapp.models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ('created_at',)
