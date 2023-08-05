import os
from pickle import TRUE
from .base import *  # noqa: F403, F401

DEBUG = True


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     },
# }

LOCAL_DEV=True
STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
STATICFILES_FINDERS=[
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATIC_URL = "/static/"

# GRAPHENE = {
#     # "SCHEMA": "grapple.schema.schema",
#     "SCHEMA": "schema.schema",
#     # 'SCHEMA': 'grapple.schema.schema',
#     # 'SUBSCRIPTION_PATH': "/ws/graphql"
#     'RELAY_CONNECTION_MAX_LIMIT': 100,
#     "MIDDLEWARE": [
#         # "grapple.middleware.GrappleMiddleware",
#         # django-graphql-jwt 需要
#         # "graphql_jwt.middleware.JSONWebTokenMiddleware",
#     ],
# }