import re
from django.forms import ModelForm, Textarea

from django import forms

from .models import Event, Meeting


class EventForm(ModelForm):
    # date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

    class Meta:
        model = Event

        fields = '__all__'

        widgets = {
            'description': Textarea(attrs={'rows': 15}),
        }

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        start = cleaned_data.get("start")
        stop = cleaned_data.get("stop")
        status = cleaned_data.get("status")
        content = cleaned_data.get("description")

        if start and stop:
            if stop < start:
                raise forms.ValidationError(
                    "La date de fin ne peut être avant la date de début"
                )

        if (not stop) and start:
            cleaned_data['stop'] = start

        if status == "r" and not start:
            raise forms.ValidationError(
                "Un événement prêt doit avoir une date de début"
            )

        expr = re.compile(r"!\[.+\]\(http:\/\/.+\)")
        matches = expr.findall(content)

        if len(matches) > 0:
            self.add_error(
                "description",
                f"La description de l'évènement contient des images en http non sécurisé ({' - '.join(matches)})"
            )


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ('OJ', 'PV')
