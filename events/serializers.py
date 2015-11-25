from .models import Event, Meeting
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'place', 'start', 'stop', 'title', 'status', 'description', 'organizer', 'meeting', 'picture')


class MeetingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Meeting
        fields = ('id', 'event', 'OJ', 'PV', "members", 'pad')
