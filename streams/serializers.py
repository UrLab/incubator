from .models import ProductTransaction
from rest_framework import serializers


class UtripSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTransaction
        fields = ('user__username','product__price')
