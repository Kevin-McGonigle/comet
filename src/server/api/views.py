from django.http import JsonResponse
from rest_framework import viewsets, status
from .models import File
from . import serializers

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
        return JsonResponse({'hash': serializer.data['hash']}, status=status.HTTP_201_CREATED, safe=False)