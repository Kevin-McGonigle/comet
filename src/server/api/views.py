from django.http import JsonResponse
from rest_framework import viewsets
from .models import File
from . import serializers

class FileUploadViewset(viewsets.ModelViewSet):
    """
    API endpoint to upload file data.
    """
    queryset = File.objects.all()
    serializer_class = serializers.FileSerializer

    def create(self, request, *args, **kwargs):
        return JsonResponse({ "hash": self.queryset[len(self.queryset) - 1].hash}, safe=False)

    def update(self, request, pk=None):
        print(request)
        pass