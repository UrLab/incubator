from rest_framework import serializers
from users.serializers import UserSerializer
from .models import SpaceStatus


class PamelaSerializer(serializers.Serializer):
    total_mac_count = serializers.IntegerField()
    last_updated = serializers.DateTimeField()
    unknown_mac = serializers.ListField(serializers.CharField())
    age = serializers.IntegerField()
    users = UserSerializer(many=True)


class SpaceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceStatus
        fields = ('time', 'is_open',)
