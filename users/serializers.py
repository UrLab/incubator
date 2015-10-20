from django.contrib.auth.models import User
from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('balance',)


#class UserSerializer(serializers.HyperlinkedModelSerializer):
#    hacker = HackerSerializer(many=False, read_only=False)
#
#    class Meta:
#        model = User
#        fields = ('id', 'username', 'email', 'hacker')
