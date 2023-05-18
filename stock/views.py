from rest_framework import viewsets
from django.shortcuts import render

from .models import Product, Category, FundZone
from .serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def payment_transaction_home(request):
    zones = FundZone.objects.all().order_by("name")
    return render(request, "transactions.html", locals())
