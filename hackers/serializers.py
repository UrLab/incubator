from django.contrib.auth.models import User
from .models import Hacker
from rest_framework import serializers


class HackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hacker
        fields = ('balance',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    hacker = HackerSerializer(many=False, read_only=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'hacker')
