from streams.serializers import UrtipSerializer
from rest_framework import viewsets

from stock.models import ProductTransaction


class UrtipViewSet(viewsets.ModelViewSet):
    queryset = ProductTransaction.objects.filter(product__category__name__iexact="urtip").order_by("when")
    serializer_class = UrtipSerializer
