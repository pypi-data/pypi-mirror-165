from django.urls import include, path
from . import views
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers
from .views import SshHostViewSet
router = routers.DefaultRouter()
router.register(r'ssh-hosts', SshHostViewSet)


urlpatterns = [
    path('', include(router.urls)), # rest_api
    path('chat_demo/',views.chat_demo, name='chat_demo'),
    path('meta/',views.meta,name='meta'),
    path('install/', views.install, name='install'),
]