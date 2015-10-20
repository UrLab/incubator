from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'balance', 'email', 'first_name', 'last_name', 'created', 'last_login')
