from stock.models import ProductTransaction
from rest_framework import serializers


class UrtipSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_price(self, obj):
        return f"{obj.product.price}€"

    class Meta:
        model = ProductTransaction
        fields = ('username', 'price')
