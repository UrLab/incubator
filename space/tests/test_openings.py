import pytest
from space.views import get_openings_df


@pytest.mark.django_db
def test_openings_empty():
    df = get_openings_df()
    assert len(df) >= 2
