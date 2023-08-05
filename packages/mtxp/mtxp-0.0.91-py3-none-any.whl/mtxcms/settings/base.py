import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import json
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
if 'SERVERTYPE' in os.environ and os.environ['SERVERTYPE'] == 'AWS Lambda':
    print("===== 远程环境？")

    # json_data = open('zappa_settings.json')
    # print(json_data)
    # env_vars = json.load(json_data)['dev']['environment_variables']
    # for key, val in env_vars.items():
    #     os.environ[key] = val


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
# Build paths inside the project like this: os.path.join(PROJECT_DIR, ...)
# os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insejja8Sla@MSKc-827DFOa907cure-yi29kbetwvqS$,A*S@yg3g-9959OPa72kAXPM!<7$A{JSKjaislxdehj@_b(#8*k%q%ap7b!$l_cms1iwt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'oauth2_provider',
    'demo',    
    'gallery',    
    "mtxauth",
    'mtx_cloud',
    "mtx_sys",
    # "mtxcms.base",
    # 'mtxcms.blog',
    'django_s3_storage',
    
]
# INSTALLED_APPS += ["django_s3_sqlite"]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',  # django-oauth-toolkit
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


AUTHENTICATION_BACKENDS = [
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
]
ROOT_URLCONF = 'mtxcms.urls'
AUTH_USER_MODEL='mtxauth.User'
LOGIN_URL='/admin/login/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'wagtail.contrib.settings.context_processors.settings',
                # 'django.template.context_processors.i18n',  # 模板中国际化相关处理器。
            ],
        },
    },
]

WSGI_APPLICATION = 'mtxcms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  'mtxcms.sqlite3',
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'mtxcms1',
    #     'USER': 'postgres',
    #     'PASSWORD': 'xIl1*yingzi606',
    #     'HOST': 'database-2.cqfetekykft2.us-east-1.rds.amazonaws.com',
    #     'PORT': '5432',
    # },
    # 'TEST': {
    #     'NAME': 'Foo',
    #     'MIGRATE': False
    # }
}

# 修改用户模型
# AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

APPEND_SLASH=False

# #############################################################################
# MTX CMS

# 默认的oauth application 名称
MTXCMS_DEFAULT_OAUTH_APP_NAME = "oiddefaultapp"
MTX_APP_ID=os.environ.get("MTX_APP_ID",  "mtxcms-default-1")
MTX_CHAT_API=os.environ.get("MTX_CHAT_API",  'wss://bajtcnb5hl.execute-api.us-east-1.amazonaws.com/chat')
MTX_WSCHAT_EVENTNAME=os.environ.get("MTX_WSCHAT_EVENTNAME",  'wss://bajtcnb5hl.execute-api.us-east-1.amazonaws.com/chat')

# --------------------------------------------------------------------------------------------
# 使用django_s3_storage处理静态文件
AWS_REGION = os.getenv('AWS_REGION', "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "AKIAX4TRZRYQ4JGAC3AI")
AWS_SECRET_ACCESS_KEY = os.getenv(
    "AWS_SECRET_ACCESS_KEY", "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")
# The optional AWS session token to use.
# AWS_SESSION_TOKEN = ""
S3_BUCKET_STATIC = f"{MTX_APP_ID}-static"
WHITENOISE_STATIC_PREFIX = '/static/'
STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
AWS_S3_BUCKET_NAME_STATIC = S3_BUCKET_STATIC
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % S3_BUCKET_STATIC
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
AWS_DEFAULT_ACL = None

# media
# if 'AWS_STORAGE_BUCKET_NAME' in os.environ:
AWS_STORAGE_BUCKET_NAME = f"{MTX_APP_ID}-storage"

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_AUTO_CREATE_BUCKET = True

INSTALLED_APPS.append('storages')
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# 下面的配置，跟 custom_storage.py 有关，在配置自定义storage 时用到。
AWS_STATIC_LOCATION = 'static'
AWS_PUBLIC_MEDIA_LOCATION = 'media'
AWS_PRIVATE_MEDIA_LOCATION = 'private'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ----------------------------------------------------------------------
# wagtail 相关设置
# WAGTAIL_SITE_NAME = "awswag"
# # 指定图片模型
# # app_name.Modelname | 获取模型：wagtail.images.get_image_model()
# WAGTAILIMAGES_IMAGE_MODEL = 'base.CustomImage'
# WAGTAILADMIN_BASE_URL = "http://localhost"


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        # # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication', # rest_framework_jwt已经不再维护了。
        # # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'mtlibs.auth0_utils.DrfAuto0Authentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
}


# 配置rest api framework 使用oauth0认证（作为api资源服务器）。
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "dev-habpxogp.us.auth0.com")
AUTH0_CLIENT_ID = os.environ.get(
    "AUTH0_CLIENT_ID", "CUdtAP4iALOlqOmeyCDhsMQmRgUFbGb8")
AUTH0_CLIENT_SECRET = os.environ.get(
    "AUTH0_CLIENT_SECRET", 'hNmgnLM0YQSQaJVyf2rxbUJmVbWg-CCFoh3z5lsQjqbFVFwlZYr-97LAHf7UAhlf')
API_IDENTIFIER = os.environ.get('API_IDENTIFIER', "http://localhost:3000")
# API_IDENTIFIER = os.environ.get('API_IDENTIFIER', "http://127.0.0.1:8000/")

PUBLIC_KEY = None
JWT_ISSUER = None

AUTH0_CLIENT_ID_WEB = AUTH0_CLIENT_ID
AUTH0_CLIENT_SECRET_WEB = AUTH0_CLIENT_SECRET


if AUTH0_DOMAIN:
    JWT_ISSUER = 'https://' + AUTH0_DOMAIN + '/'
# auth0
# JWT_AUTH = {
#     'JWT_PAYLOAD_GET_USERNAME_HANDLER':
#         'auth0authorization.utils.jwt_get_username_from_payload_handler',
#     'JWT_DECODE_HANDLER':
#         'auth0authorization.utils.jwt_decode_token',
#     'JWT_ALGORITHM': 'RS256',
#     'JWT_AUDIENCE': API_IDENTIFIER,
#     'JWT_ISSUER': JWT_ISSUER,
#     'JWT_AUTH_HEADER_PREFIX': 'Bearer',
# }

# SIMPLE_JWT = {
#     'JWT_PAYLOAD_GET_USERNAME_HANDLER':
#         'auth0authorization.utils.jwt_get_username_from_payload_handler',
#     'JWT_DECODE_HANDLER':
#         'auth0authorization.utils.jwt_decode_token',
#     'JWT_ALGORITHM': 'RS256',
#     'JWT_AUDIENCE': API_IDENTIFIER,
#     'JWT_ISSUER': JWT_ISSUER,
#     'JWT_AUTH_HEADER_PREFIX': 'Bearer',
# }


#############################################################################
# django-cors-headers 相关配置
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORE_ALLOW_CREDENTIALS = True

# oauth toolkit 设置 oidc 特别是私钥
OAUTH2_PROVIDER = {
    "OIDC_ENABLED": True,
    # os.environ.get("OIDC_RSA_PRIVATE_KEY"),
    "OIDC_RSA_PRIVATE_KEY": 'privatekey112988snajdfhA@#asdjnh8a9',
    "SCOPES": {
        "openid": "OpenID Connect scope",
        # ... any other scopes that you use
    },
    "ACCESS_TOKEN_EXPIRE_SECONDS": 86400  # 86400 second=24h (default 36000s)
    # ... any other settings you want
}

# GRAPHENE = {
#     # "SCHEMA": "grapple.schema.schema",
#     # "SCHEMA": "djmain.schema.schema",
#     # 'SCHEMA': 'grapple.schema.schema',
#     'SCHEMA': 'mtx_cloud.schema.schema',
#     # 'SUBSCRIPTION_PATH': "/ws/graphql"
#     'RELAY_CONNECTION_MAX_LIMIT': 100,
#     "MIDDLEWARE": [
#         "grapple.middleware.GrappleMiddleware",
#         # django-graphql-jwt 需要
#         # "graphql_jwt.middleware.JSONWebTokenMiddleware",
#     ],
# }
# GRAPPLE = {
#     "APPS": ["base", "blog", "mtxauth"],
#     "ADD_SEARCH_HIT": True,
#     "EXPOSE_GRAPHIQL": True,
# }

PAPERLESS_URL="https://ecs1.csrep.top"