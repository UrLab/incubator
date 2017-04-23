import uuid
import json

from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from space.models import PrivateAPIKey
from users.models import User

import pytest

from space.decorators import private_api

X = HttpResponse('{"test": "i am the inner fn"}', content_type="application/json")
Y = HttpResponse('this is not json')


@private_api()
def inner_fn(request):
    return X


@private_api()
def bad_view(request):
    return Y


def j(response):
    return json.loads(response.content.decode())


@pytest.fixture(scope='function')
def secret():
    secret = PrivateAPIKey.objects.create(
        user=User.objects.create(
            username="test user"
        ),
        name="My test key",
        active=True
    )
    return secret.key


def test_get(rf):
    request = rf.get('')
    response = inner_fn(request)
    assert response.status_code == 400
    assert j(response)['error'] == "Only POST requests are allowed"


def test_no_secret(rf):
    request = rf.post('')
    response = inner_fn(request)
    assert response.status_code == 400
    assert j(response)['error'] == "Missing 'secret' param"


@pytest.mark.django_db
def test_not_uuid_secret(rf, secret):
    bad_secret = 'this-is-a-bad-secret-and-not-an-uuid'
    request = rf.post('', {'secret': bad_secret})
    response = inner_fn(request)
    assert response.status_code == 400
    assert j(response)['error'] == 'Bad secret {} is not an uuid'.format(bad_secret)


@pytest.mark.django_db
def test_bad_secret(rf, secret):
    bad_secret = uuid.uuid4()
    request = rf.post('', {'secret': bad_secret})
    response = inner_fn(request)
    assert response.status_code == 403
    assert j(response)['error'] == 'Bad secret {} is not in the allowed list'.format(bad_secret)


@pytest.mark.django_db
def test_simple(rf, secret):
    request = rf.post('', {'secret': secret})
    response = inner_fn(request)
    assert type(response) == HttpResponse
    assert response == X


@pytest.mark.django_db
def test_content_type(rf, secret):
    request = rf.post('', {'secret': secret})
    with pytest.raises(AssertionError):
        bad_view(request)


@pytest.mark.django_db
def test_cast(rf, secret):
    @private_api(var=float)
    def inner_fn(request, var):
        assert isinstance(var, float)
        assert var == 1.1
        return X

    request = rf.post('', {'secret': secret, 'var': '1.1'})
    response = inner_fn(request)
    assert type(response) == HttpResponse
    assert response == X


@pytest.mark.django_db
def test_does_not_strip_args(rf, secret):
    @private_api(var=float)
    def inner_fn(request, fixed_var, fixed_named, var):
        assert isinstance(var, float)
        assert var == 1.1
        assert fixed_var == '42'
        assert fixed_named == 'ololol'
        return X

    request = rf.post('', {'secret': secret, 'var': '1.1'})
    response = inner_fn(request, '42', fixed_named='ololol')
    assert type(response) == HttpResponse
    assert response == X


@pytest.mark.django_db
def test_missing_post_arg(rf, secret):
    @private_api(var=float)
    def inner_fn(request, var):
        assert isinstance(var, float)
        assert var == 1.1
        return X

    request = rf.post('', {'secret': secret})
    response = inner_fn(request)
    assert response.status_code == 400
    assert j(response)['error'] == 'Parameter var is required'
