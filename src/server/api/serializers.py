from rest_framework import serializers
from .models import File

class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['hash', 'name', 'type', 'when_uploaded', 'file']

    