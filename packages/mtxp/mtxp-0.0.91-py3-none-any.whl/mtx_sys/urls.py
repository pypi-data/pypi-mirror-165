from django.urls import path
# from graphene_django.views import GraphQLView

from django.urls import include, path
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
# from . import schema

# schema = schema.create_schema()

urlpatterns = [
    path('mtxsys', views.index, name='index'),
]
