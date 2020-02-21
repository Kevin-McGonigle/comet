from rest_framework import serializers
from .models import File, FileHash

class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['hash', 'name', 'size', 'file_type', 'when_uploaded', 'file']

class FileHashSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileHash
        fields = ['hash']