import uuid

from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from space.models import PrivateAPIKey
from users.models import User

import pytest

from space.decorators import private_api
X = HttpResponse('i am the inner fn')


@private_api()
def inner_fn(request):
    return X


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
    assert isinstance(response, HttpResponseBadRequest)
    assert response.content == b"Only POST is allowed"


def test_no_secret(rf):
    request = rf.post('')
    response = inner_fn(request)
    assert isinstance(response, HttpResponseBadRequest)
    assert response.content == b"You must query this endpoint with a secret."


@pytest.mark.django_db
def test_not_uuid_secret(rf, secret):
    bad_secret = 'this-is-a-bad-secret-and-not-an-uuid'
    request = rf.post('', {'secret': bad_secret})
    response = inner_fn(request)
    assert isinstance(response, HttpResponseBadRequest)
    assert response.content == bytes('Bad secret {} is not an uuid'.format(bad_secret), 'utf-8')


@pytest.mark.django_db
def test_bad_secret(rf, secret):
    bad_secret = uuid.uuid4()
    request = rf.post('', {'secret': bad_secret})
    response = inner_fn(request)
    assert isinstance(response, HttpResponseForbidden)
    assert response.content == bytes('Bad secret {} is not in the allowed list'.format(bad_secret), 'utf-8')


@pytest.mark.django_db
def test_simple(rf, secret):
    request = rf.post('', {'secret': secret})
    response = inner_fn(request)
    assert type(response) == HttpResponse
    assert response == X


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
    assert isinstance(response, HttpResponseBadRequest)
    assert response.content == b'Parameter var is required'
