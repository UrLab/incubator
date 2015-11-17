from rest_framework import serializers
from users.serializers import UserSerializer


class PamelaSerializer(serializers.Serializer):
    total_mac_count = serializers.IntegerField()
    last_updated = serializers.DateTimeField()
    unknown_mac = serializers.ListField(serializers.CharField())
    users = UserSerializer(many=True)
