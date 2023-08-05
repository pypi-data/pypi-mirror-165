import os
from .base import *  # noqa: F403, F401

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# BASE_URL required for notification emails
# BASE_URL = 'https://wagtail.csrep.top'

ALLOWED_HOSTS = ['*']
# CSRF_TRUSTED_ORIGINS = ["https://wagtail-dev.csrep.top"]

# CSRF_TRUSTED_ORIGINS = ["https://*.csrep.top"]
CORS_ORIGIN_ALLOW_ALL = True

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# sqlitedb_path = os.path.join(BASE_DIR, '..',  'mtxdb2.dev.sqlite3')
sqlitedb_path = os.path.join('/dev/shm/myproject.test.db.sqlite3')

# print(f"数据库路径：{sqlitedb_path}")
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': sqlitedb_path,
    }
}
