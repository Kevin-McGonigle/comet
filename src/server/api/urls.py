from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'api/upload', views.FileUploadViewset, 'upload')
router.register(r'api/file', views.FileInformationViewset, 'file')
router.register(r'api/method', views.MethodViewpoint, 'method')
router.register(r'api/class', views.ClassViewpoint, 'class')

urlpatterns = [
    path('', include(router.urls))
]