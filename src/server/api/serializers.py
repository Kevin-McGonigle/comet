from rest_framework import serializers

from .models import File, Method, Class


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['hash', 'name', 'size', 'file_type', 'when_uploaded', 'file']


class MethodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Method
        fields = ['method_hash', 'parent', 'name', 'arguments', 'returns', 'child_hash']


class ClassSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Class
        fields = ['class_hash', 'parent', 'name', 'arguments', 'methods', 'returns', ' child_hash']
