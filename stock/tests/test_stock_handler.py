from django.http import HttpResponse, HttpResponseBadRequest
from django.http.response import Http404
from space.models import PrivateAPIKey
from users.models import User
from stock.models import Product, Category
from stock.views import buy_product_with_stock_handler, product_infos

import pytest
import json


def fib(n, x1=0, x2=1):
    for i in range(n):
        yield x1
        x1, x2 = x2, x1+x2
        n -= 1

USER_QR = ''.join(map(str, fib(5)))
PRODUCT_BARCODE = ''.join(map(str, fib(5, 4, 6)))


@pytest.fixture(scope='function')
def secret():
    user = User.objects.create(username="QR user", qrcode=USER_QR)
    secret = PrivateAPIKey.objects.create(user=user, name="Key", active=True)
    Product.objects.create(
        category=Category.objects.create(name="category"),
        name="product",
        price=4.2,
        barcode=PRODUCT_BARCODE
    )
    return secret.key


@pytest.mark.django_db
def test_buy_product(rf, secret):
    request = rf.post('', {'secret': secret,
                           'user_qrcode': USER_QR,
                           'product_barcode': PRODUCT_BARCODE,
                           'quantity': 1})
    response = buy_product_with_stock_handler(request)
    assert type(response) == HttpResponse


@pytest.mark.django_db
def test_no_product(rf, secret):
    request = rf.post('', {'secret': secret,
                           'user_qrcode': USER_QR,
                           'product_barcode': "007",
                           'quantity': 1})
    with pytest.raises(Http404):
        buy_product_with_stock_handler(request)


@pytest.mark.django_db
def test_no_user(rf, secret):
    request = rf.post('', {'secret': secret,
                           'user_qrcode': "007",
                           'product_barcode': PRODUCT_BARCODE,
                           'quantity': 1})
    with pytest.raises(Http404):
        buy_product_with_stock_handler(request)


@pytest.mark.django_db
def test_negative_quantity(rf, secret):
    request = rf.post('', {'secret': secret,
                           'user_qrcode': USER_QR,
                           'product_barcode': PRODUCT_BARCODE,
                           'quantity': -1})
    response = buy_product_with_stock_handler(request)
    assert type(response) == HttpResponseBadRequest


@pytest.mark.django_db
def test_zero_quantity(rf, secret):
    request = rf.post('', {'secret': secret,
                           'user_qrcode': USER_QR,
                           'product_barcode': PRODUCT_BARCODE,
                           'quantity': 0})
    response = buy_product_with_stock_handler(request)
    assert type(response) == HttpResponseBadRequest


@pytest.mark.django_db
def test_product_info(rf, secret):
    request = rf.get('')
    response = product_infos(request, PRODUCT_BARCODE)
    data = json.loads(response.content.decode())
    assert data['price'] == 4.2
    assert data['name'] == 'product'
    assert data['category'] == 'category'
