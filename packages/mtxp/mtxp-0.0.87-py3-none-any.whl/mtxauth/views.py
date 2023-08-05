from rest_framework import serializers, viewsets, routers
from django.contrib.auth.models import User
import os
import json
import time
import math
import requests
from requests import request
import django
from authlib.integrations.django_client import OAuth
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render

from urllib.parse import quote_plus, urlencode
from django import forms
# from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
# from django.utils import timezone
from django.forms.models import model_to_dict
from django.contrib import auth
from mtlibs import auth0_utils
import jwt
from jwt import PyJWKClient
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,schema
from rest_framework.response import Response
import logging
logger = logging.getLogger(__name__)
User = get_user_model()
oauth = OAuth()


@csrf_exempt
@api_view(['POST'])
def signin(request):
    """自定义jwt签发的方式登录"""
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            username = json_data.get('username', None)
            password = json_data.get('password', None)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                user.get_username()
                encoded_jwt = jwt.encode(
                    {"username": user.get_username()}, settings.SECRET_KEY, algorithm="HS256")
                return JsonResponse({"token": encoded_jwt})
            
        except Exception as e:
            logger.info(f'signin error {e}')

    return Response({"token":None})


@csrf_exempt
def signup(request):
    """自定义jwt签发的方式注册"""
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            username = json_data.get('username', None)
            password = json_data.get('password', None)
            email = json_data.get("email", None)

            existsUser = User.objects.filter(username=username).first()
            if existsUser:
                logger.info(f'注册失败，用户已经存在 {existsUser.get_username()}')
                return JsonResponse({
                    "success": False,
                    "message": "注册失败，用户已存在"
                })

            user = User.objects.create(
                username=username,
                password=password,
                email=email
            )
            user.save()
            encoded_jwt = jwt.encode(
                {"username": user.get_username()}, settings.SECRET_KEY, algorithm="HS256")
            return JsonResponse({"success": True, "token": encoded_jwt})

        except Exception as e:
            logger.info(f'signin error {e}')

    return HttpResponse("")

@csrf_exempt
@api_view(['GET'])
def me(request):
    return Response({
        "username": request.user.get_username(),
        "message": "Will not appear in schema!"
    })
 

@api_view(['GET'])
@schema(None)
def view1(request):
    return Response({"message": "Will not appear in schema!"})

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID_WEB,
    client_secret=settings.AUTH0_CLIENT_SECRET_WEB,
    client_kwargs={
        "scope": "openid profile email read:messages",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def oauth0_home(request):
    """看看登录情况"""

    return render(
        request,
        "mtxauth/oauth0_index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )


def login_oauth0(request):
    # 注意：由于反向代理的关系，这里得到的完整url可能跟公网地址不一致。
    url = request.build_absolute_uri(reverse("callback"))
    # url=""
    return oauth.auth0.authorize_redirect(request, url)


def callback(request):
    """oauth0 登录后回调"""
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token

    # 补充，上面是使用oauth0登录进来的用户，现在创建一个对应的系统用户数据与之对应

    username = token["userinfo"]["name"]
    email = token["userinfo"]["email"]

    user = User.objects.filter(username=username).first()
    default_password = "123456789ABC123"
    if not user:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=default_password)

    auth.login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    # authentied_user = auth.authenticate(request,username=username, password=default_password)
    # if authentied_user is not None:
    # auth.login(request, user)
    # auth.authenticate(request, user)

    # if user：
    # auth.login(request, user)

    # access_token = token["access_token"]
    # tt = auth0_utils.jwt_decode_token2(access_token)
    # print(tt)
    return redirect(request.build_absolute_uri(reverse("home")))


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("home")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


def oauth0_debug(request):

    access_token = request.session["user"]["access_token"]
    id_token = request.session["user"]["id_token"]

    response = requests.get(f"https://{settings.AUTH0_DOMAIN}/userinfo", headers={
        "Authorization": "Bearer {access_token}"
    })

    responseJson = response.content.decode()

    return JsonResponse({
        "AUTH0_DOMAIN": settings.AUTH0_DOMAIN,
        "baseurl": reverse("callback"),
        # "settings.BASE_URL": settings.BASE_URL,
        "url3": request.build_absolute_uri(reverse("callback")),
        "access_token": access_token,
        "id_token": id_token,
        "responseJson": responseJson
    })


def oauth0_debug2(request):
    return HttpResponse(request, "mtxauth/debug1.html")


def oauth0_userinfo(request):
    """
        根据传入的token，请求auth0获取当前用户信息。
        思考：
            1: idtoken 应该包含详细的用户信息。是否能够在这里解码得到用户信息，而不用请求auth0 api？
    """
    token = auth0_utils.get_token_auth_header(request)
    response = requests.get(f"https://{settings.AUTH0_DOMAIN}/userinfo", headers={
        "Authorization": f"Bearer {token}"
    })
    responseJson = response.content.decode()
    return HttpResponse(responseJson)


@login_required()
def oauth_tookkit_me(request, *args, **kwargs):
    """根据 Authorization token 获取当前用户信息, ( oauth toolkit )"""
    return JsonResponse({
        "username": request.user.username,
        "backend": request.user.backend
    })


def decode_auto0_token(request):
    """试验：直接解码传入的Authorization token，查看到底是什么。"""
    token = auth0_utils.get_token_auth_header(request)
    data = auth0_utils.jwt_decode_token2(token)
    return JsonResponse({"decode_token": data})


def decode_auto0_token2(request):
    """试验：直接解码传入的Authorization token，查看到底是什么。"""
    token = auth0_utils.get_token_auth_header(request)
    data = auth0_utils.jwt_decode_token(token)
    return JsonResponse({"decode_token": data})
