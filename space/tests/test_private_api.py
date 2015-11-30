from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse

from space.decorators import private_api
X = HttpResponse('i am the inner fn')


@private_api()
def inner_fn(request):
    return X


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


def test_bad_secret(rf, settings):
    settings.STATUS_SECRETS = ['good_secret1', 'good_secret2']
    request = rf.post('', {'secret': 'bad_secret'})
    response = inner_fn(request)
    assert isinstance(response, HttpResponseForbidden)
    assert response.content == b'Bad secret bad_secret is not in the allowed list'


def test_simple(rf, settings):
    settings.STATUS_SECRETS = ['good_secret1', 'good_secret2']

    request = rf.post('', {'secret': 'good_secret1'})
    response = inner_fn(request)
    assert isinstance(response, HttpResponse)
    assert response == X


def test_cast(rf, settings):
    settings.STATUS_SECRETS = ['good_secret1', 'good_secret2']

    @private_api(var=float)
    def inner_fn(request, var):
        assert isinstance(var, float)
        assert var == 1.1
        return X

    request = rf.post('', {'secret': 'good_secret1', 'var': '1.1'})
    response = inner_fn(request)
    assert isinstance(response, HttpResponse)
    assert response == X


def test_does_not_strip_args(rf, settings):
    settings.STATUS_SECRETS = ['good_secret1', 'good_secret2']

    @private_api(var=float)
    def inner_fn(request, fixed_var, fixed_named, var):
        assert isinstance(var, float)
        assert var == 1.1
        assert fixed_var == '42'
        assert fixed_named == 'ololol'
        return X

    request = rf.post('', {'secret': 'good_secret1', 'var': '1.1'})
    response = inner_fn(request, '42', fixed_named='ololol')
    assert isinstance(response, HttpResponse)
    assert response == X
