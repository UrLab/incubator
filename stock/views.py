from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from actstream import action

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from space.decorators import private_api, validate
from users.models import User


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def product_infos(request, product_barcode):
    prod = get_object_or_404(Product, barcode=product_barcode)
    return JsonResponse({
        'name': prod.name,
        'category': prod.category.name,
        'price': float(prod.price),
    })


@private_api(user_qrcode=str, product_barcode=str, quantity=validate(int, lambda x: x > 0))
def buy_product_with_stock_handler(request, user_qrcode, product_barcode, quantity):
    prod = get_object_or_404(Product, barcode=product_barcode)
    user = get_object_or_404(User, qrcode=user_qrcode)
    user.balance -= quantity * prod.price
    user.save()
    action.send(
        user,
        verb="a acheté {} pour {}€".format(prod.name, prod.price),
        public=False
    )
    return HttpResponse("ok")
