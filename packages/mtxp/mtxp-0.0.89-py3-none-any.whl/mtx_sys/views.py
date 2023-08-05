from django.shortcuts import render

from django.http import HttpResponse,FileResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse


import jwt
from functools import wraps

from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

def index(request):
    return "mtx sys home"

