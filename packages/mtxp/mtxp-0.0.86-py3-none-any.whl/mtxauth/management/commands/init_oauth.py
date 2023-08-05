import os
from unicodedata import name

from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from django.contrib.auth import get_user_model
User = get_user_model()
from oauth2_provider.models import AccessToken, Application
from django.conf import settings
from mtlibs import oauthHelper
class Command(BaseCommand):
    @atomic
    def handle(self, **options):
        """oauth 环境进行必要的初始化设置。
        """
        oauthHelper.setup_default_app()
        
        
