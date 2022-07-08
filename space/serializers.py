from rest_framework import serializers
from users.serializers import UserSerializer
from .models import SpaceStatus, MusicOfTheDay


class PamelaSerializer(serializers.Serializer):
    total_mac_count = serializers.IntegerField()
    last_updated = serializers.DateTimeField()
    unknown_mac = serializers.ListField(child=serializers.CharField())
    age = serializers.IntegerField()
    users = UserSerializer(many=True)
    hidden = serializers.IntegerField()


class SpaceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceStatus
        fields = ('time', 'is_open',)


class MotdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicOfTheDay
        fields = ('url', 'irc_nick', 'day')
