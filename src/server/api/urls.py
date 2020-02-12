from django.urls import path

from .views import *

urlpatterns = [
    path('file/', file),
    path('file/<str:pk>/', file_detail),
    path('class/', class_),
    path('class/<str:pk>/', class_detail),
    path('method/', method),
    path('method/<str:pk>/', method_detail),
]