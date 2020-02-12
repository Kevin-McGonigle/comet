from rest_framework import serializers

from .models import *


class FileSerializer(serializers.Serializer):
    hash = serializers.CharField(max_length=64)
    name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=255)
    when_uploaded = serializers.DateTimeField()
    file = serializers.FileField()

    def create(self, validated_data):
        return File.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.hash = validated_data.get("hash", instance.hash)
        instance.name = validated_data.get("name", instance.name)
        instance.type = validated_data.get("type", instance.type)
        instance.when_uploaded = validated_data.get("when_uploaded", instance.when_uploaded)
        instance.file = validated_data.get("file", instance.file)
        instance.save()
        return instance


class ClassSerializer(serializers.Serializer):
    hash = serializers.CharField(max_length=64)
    file_hash = serializers.CharField(max_length=64)
    name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Class.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.hash = validated_data.get("hash", instance.hash)
        instance.file_hash = validated_data.get("file_hash", instance.file_hash)
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class MethodSerializer(serializers.Serializer):
    hash = serializers.CharField(max_length=64)
    class_hash = serializers.CharField(max_length=64, default="")
    file_hash = serializers.CharField(max_length=64)
    name = serializers.CharField(max_length=64)
    return_type = serializers.CharField(max_length=255, default="void")

    def create(self, validated_data):
        return Method.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.hash = validated_data.get("hash", instance.hash)
        instance.class_hash = validated_data.get("class_hash", instance.class_hash)
        instance.file_hash = validated_data.get("file_hash", instance.file_hash)
        instance.name = validated_data.get("name", instance.name)
        instance.return_type = validated_data.get("return_type", instance.return_type)
        instance.save()
        return instance


class MethodParameterSerializer(serializers.Serializer):
    method_hash = serializers.CharField(max_length=64)
    name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return MethodParameter.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.method_hash = validated_data.get("method_hash", instance.method_hash)
        instance.name = validated_data.get("name", instance.name)
        instance.type = validated_data.get("type", instance.type)
        instance.save()
        return instance


class ClassRelationshipSerializer(serializers.Serializer):
    parent_hash = serializers.CharField(max_length=64)
    child_hash = serializers.CharField(max_length=64)
    relationship_type = serializers.CharField(max_length=255, default="association")

    def create(self, validated_data):
        return ClassRelationship.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.parent_hash = validated_data.get("parent_hash", instance.parent_hash)
        instance.child_hash = validated_data.get("child_hash", instance.child_hash)
        instance.relationship_type = validated_data.get("relationship_type", instance.relationship_type)
        instance.save()
        return instance
