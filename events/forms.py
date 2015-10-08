from django.forms import ModelForm
from django import forms

from .models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['organizer']

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        start = cleaned_data.get("start")
        stop = cleaned_data.get("stop")
        status = cleaned_data.get("status")

        if start and stop:
            if stop < start:
                raise forms.ValidationError(
                    "La date de fin ne peut être avant la date de début"
                )

        if (not stop) and start:
            cleaned_data['stop'] = start

        if status in ("r", "p") and not start:
            raise forms.ValidationError(
                "Un événement prêt ou planifié doit avoir une date de début"
            )
