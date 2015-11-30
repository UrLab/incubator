from events.forms import EventForm
from datetime import datetime
import pytest
from users.models import User


@pytest.fixture(scope='function')
def user():
    user = User.objects.create(username="test", email="test@test.be", first_name="Test", last_name="Test")
    return user.id


@pytest.mark.django_db
def test_only_title_and_state_required(user):
    form_data = {
        'title': 'wtf',
        'status': 'i',
        'organizer': user,
    }
    form = EventForm(data=form_data)

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_no_stop_but_start(user):
    form_data = {
        'title': 'wtf',
        'status': 'i',
        'start': datetime(2000, 1, 1),
        'organizer': user,
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
    assert 'Un événement prêt doit avoir une date de début' in form.errors['__all__']


def test_stop_must_be_after_start():
    form_data = {
        'title': 'wtf',
        'status': 'i',
        'start': datetime(2100, 1, 1),
        'stop': datetime(2000, 1, 1)
    }
    form = EventForm(data=form_data)

    assert not form.is_valid()
    assert 'La date de fin ne peut être avant la date de début' in form.errors['__all__']
