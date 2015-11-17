from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    gravatar = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('username', 'gravatar', 'has_key')
