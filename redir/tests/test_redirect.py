from django.http import HttpResponseRedirect
from django.test import Client
from redir.models import Redirection
import pytest


@pytest.fixture(scope='function')
def redir():
    return Redirection.objects.create(name='test', target="http://test.com/")


@pytest.mark.django_db
def test_valid_redir(redir):
    res = Client().get('/r/{}'.format(redir.name))
    assert isinstance(res, HttpResponseRedirect)


@pytest.mark.django_db
def test_invalid_redir():
    res = Client().get('/trolilol')
    assert not isinstance(res, HttpResponseRedirect)
