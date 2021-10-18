import pytest
# from space.plots import get_openings_df
from space.models import SpaceStatus


@pytest.mark.django_db
def test_openings_empty():
    # df = get_openings_df('2012-12-21', '2012-12-28')
    # assert len(df) == 1 + 24 * 7
    # assert not df.is_open.any()
    True is True


@pytest.mark.django_db
def test_openings_week():
    # First complete sept week 2016: monday 05/09 to sunday 11/09
    openings = [
        {'time': '2016-09-05 10:00:00.0000+02:00', 'is_open': True},
        {'time': '2016-09-05 18:00:00.0000+02:00', 'is_open': False},
        {'time': '2016-09-05 19:30:00.0000+02:00', 'is_open': True},
        {'time': '2016-09-05 21:00:00.0000+02:00', 'is_open': False},
    ]

    begin, end = '2016-09-05 00:00:00.0000+02:00', '2016-09-11 00:00:00.0000+02:00'

    SpaceStatus.objects.bulk_create(SpaceStatus(**x) for x in openings)
    in_week = SpaceStatus.objects.filter(time__gte=begin, time__lte=end)
    assert in_week.count() == 4

    # df = get_openings_df(begin, end)

    # assert not df['2016-09-05 09:00':'2016-09-05 09:59'].is_open.any()
    # assert df['2016-09-05 10:00':'2016-09-05 10:59'].is_open.all()
