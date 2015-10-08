from events.forms import EventForm
from datetime import datetime


def test_only_title_and_state_required():
    form_data = {
        'title': 'wtf',
        'status': 'j'
    }
    form = EventForm(data=form_data)

    assert form.is_valid(), form.errors


def test_no_stop_but_start():
    form_data = {
        'title': 'wtf',
        'status': 'j',
        'start': datetime(2000, 1, 1)
    }
    form = EventForm(data=form_data)

    assert form.is_valid(), form.errors
    assert form.cleaned_data['start'] == form.cleaned_data['stop']
    assert form.cleaned_data['start'].year == 2000


def test_ready_must_have_date():
    form_data = {
        'title': 'wtf',
        'status': 'r',
    }
    form = EventForm(data=form_data)

    assert not form.is_valid(), form.errors
    assert 'Un événement prêt ou planifié doit avoir une date de début' in form.errors['__all__']


def test_stop_must_be_after_start():
    form_data = {
        'title': 'wtf',
        'status': 'j',
        'start': datetime(2100, 1, 1),
        'stop': datetime(2000, 1, 1)
    }
    form = EventForm(data=form_data)

    assert not form.is_valid()
    assert 'La date de fin ne peut être avant la date de début' in form.errors['__all__']
