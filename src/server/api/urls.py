from django.urls import include, path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from . import views

router = routers.DefaultRouter()
router.register(r'api/upload', views.FileUploadViewset, 'upload')
router.register(r'api/file', views.FileHashViewset, 'file')

schema_view = get_swagger_view(title="Comet API")

urlpatterns = [
    path('api/docs/', schema_view),
    path('', include(router.urls))
]