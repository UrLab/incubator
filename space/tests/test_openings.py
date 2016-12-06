import pytest
from space.plots import weekday_probs
from space.models import SpaceStatus, SpaceStatusPrediction
from django.core.management import call_command
from django.utils import timezone


@pytest.mark.django_db
def test_openings_empty():
    sr = weekday_probs({})
    assert len(sr) == 0
    assert not sr.any()


@pytest.mark.django_db
def test_openings_prediction():
    openings = [
        {'time': '2016-09-05 10:00', 'is_open': True},
        {'time': '2016-09-05 18:00', 'is_open': False},
        {'time': '2016-09-05 19:30', 'is_open': True},
        {'time': '2016-09-05 21:00', 'is_open': False},
    ]
    SpaceStatus.objects.bulk_create(SpaceStatus(**x) for x in openings)
    call_command("predict_openings")

    ssps = SpaceStatusPrediction.objects.all()
    assert(len(ssps) == 168)
    now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    next_week = now + timezone.timedelta(days=7)
    for ssp in ssps:
        assert(0 <= ssp.proba_open <= 1)
        assert(now <= ssp.time < next_week)

    sr = weekday_probs({})
    assert(len(sr) == 24)
    for p in sr:
        assert(0 <= p <= 1)