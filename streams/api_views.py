from streams.serializers import UtripSerializer
from rest_framework import viewsets


class UtripViewSet(viewsets.ModelViewSet):
    queryset = ProductTransaction.objects.filter(product__category__name="utrip").sort_by("when")
    serializer_class = UtripSerializer
