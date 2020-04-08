from django.http import JsonResponse
from rest_framework import viewsets, status
from .models import File, Method, Class
from . import serializers
import json

class FileUploadViewset(viewsets.ModelViewSet):
    """
    API endpoint to upload file data.
    """
    queryset = File.objects.all()
    serializer_class = serializers.FileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # file_manager = Manager(self.queryset.get(hash=serializer.data['hash']).file)
        # comet_result = file_manager.generate_comet_result()
        return JsonResponse({'hash': serializer.data['hash'], 'content': serializer.data['file']}, status=status.HTTP_201_CREATED, safe=False)

class FileInformationViewset(viewsets.ModelViewSet):
    """
    API endpoint to return a file's information from a given hash
    """
    serializer_class = serializers.FileSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            file_hash = self.request.GET.get('hash', None)
            if file_hash is not None:
                return File.objects.all().filter(hash=file_hash)

            return File.objects.all()
            

class MethodViewpoint(viewsets.ModelViewSet):
    """
    API endpoint to return a method's information from a given hash
    """
    serializer_class = serializers.MethodSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            method_hash = self.request.GET.get('method_hash', None)
            if method_hash is not None:
                return Method.objects.all().filter(method_hash=method_hash)
            
            return Method.objects.all()


class ClassViewpoint(viewsets.ModelViewSet):
    """
    API endpoint to return a class' information from a given hash
    """
    serializer_class = serializers.ClassSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse({'hash': serializer.data['class_hash']}, status=status.HTTP_201_CREATED, safe=False)

    def get_queryset(self):
        if self.request.method == "GET":
            class_hash = self.request.GET.get('class_hash', None)
            if class_hash is not None:
                return Class.objects.all().filter(class_hash=class_hash)
            
            return Class.objects.all()
