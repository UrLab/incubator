from .models import Event
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'place', 'start', 'stop', 'title', 'status', 'description', 'organizer')
