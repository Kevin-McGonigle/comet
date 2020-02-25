from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'api/upload', views.FileUploadViewset, 'upload')
router.register(r'api/file', views.FileInformationViewset, 'file')

urlpatterns = [
    path('', include(router.urls))
]