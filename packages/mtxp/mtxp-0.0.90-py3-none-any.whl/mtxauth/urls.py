from .views import UserViewSet
from django.urls import include, path
from . import views
from rest_framework import serializers, viewsets, routers
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),  # rest_api
    path('signin/', views.signin, name="signin"),  # 自定义登录（JWT）
    path('signup/', views.signup, name="signup"),  # 自定义注册（JWT）
    path("me/", views.me),
    
    path("home/", views.oauth0_home, name="home"),
    path("login/", views.login_oauth0, name="login"),
    path("logout/", views.logout, name="logout"),
    path("callback/", views.callback, name="callback"),
    path("debug/", views.oauth0_debug, name="oauth0_debug"),
    path("oauth0_userinfo/", views.oauth0_userinfo, name="oauth0_userinfo"),
    
    path("decode_token/", views.decode_auto0_token, name="oauth0_token_decode"),
    path("decode_token2/", views.decode_auto0_token2,
         name="oauth0_token_decode2"),
    
    path("view1/",views.view1),

    # path("signin/", views.signin, name="auth_signin")
]
