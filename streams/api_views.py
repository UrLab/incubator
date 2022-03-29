from streams.serializers import UtripSerializer
from rest_framework import viewsets

from stock.models import ProductTransaction


class UtripViewSet(viewsets.ModelViewSet):
    queryset = ProductTransaction.objects.filter(product__category__name="utrip").order_by("when")
    serializer_class = UtripSerializer
