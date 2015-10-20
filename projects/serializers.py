from .models import Project
from rest_framework import serializers


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'maintainer', 'participants', 'status', 'progress', 'short_description', 'content')
