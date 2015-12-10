from .models import Event, Meeting
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'place', 'start', 'stop', 'title', 'status', 'description', 'organizer', 'meeting', 'picture')


class HackerAgendaEventSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_full_url', read_only=True)
    end = serializers.DateTimeField(source='stop', read_only=True)
    location = serializers.CharField(source='place', read_only=True)
    all_day = serializers.BooleanField()

    class Meta:
        model = Event
        fields = ('title', 'start', 'end', 'all_day', 'url', 'location')


class MeetingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Meeting
        fields = ('id', 'event', 'OJ', 'PV', "members", 'pad')


class FullMeetingSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = Meeting
        fields = ('id', 'OJ', 'PV', 'pad', "event", "members")
