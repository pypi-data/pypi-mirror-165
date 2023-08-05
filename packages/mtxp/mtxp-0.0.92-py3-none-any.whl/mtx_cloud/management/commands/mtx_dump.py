import os
import boto3
from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from wagtail.core.models import Page, Site
import tempfile
from mtlibs.aws import s3_helper
import time



class Command(BaseCommand):

    help = 'dump 数据库，保存到 s3 storage 上。'
    
    def __init__(self):
        
        self.app_id=settings.MTX_APP_ID
        self.bucket = f"{self.app_id}-storage"
    def dump_db(self):
        dumpfile = tempfile.mktemp(suffix=".json")
        print(f"dumpfile to {dumpfile}")
        # fixtures_dir = os.path.join(settings.PROJECT_DIR, 'mtxcmscore', 'fixtures')
        # fixture_file = os.path.join(fixtures_dir, 'mydump.json')

        # print("Copying media files to configured storage...")
        # local_storage = FileSystemStorage(os.path.join(fixtures_dir, 'media'))
        # self._copy_files(local_storage, '')  # file storage paths are relative

        # Wagtail creates default Site and Page instances during install, but we already have
        # # them in the data load. Remove the auto-generated ones.
        # if Site.objects.filter(hostname='localhost').exists():
        #     Site.objects.get(hostname='localhost').delete()
        # if Page.objects.filter(title='Welcome to your new Wagtail site!').exists():
        #     Page.objects.get(title='Welcome to your new Wagtail site!').delete()

        call_command('dumpdata',
                     "-e", "wagtailsearch",
                     "-e", "contenttypes",
                     "-e", "sessions",
                     "-e", "admin",                 # exclude history of admin actions on admin site
                     "-e", "wagtailcore.locale",    # locale 导入时报错：Locale matching query does not exist
                     "-e", 'auth.Permission',       # 这个会自动重建，没必要导出。
                     "--indent", "2",
                     #  "--natural",    # 这个不知道具体能起什么作用
                     "-o", dumpfile,
                     verbosity=1)

        # 上传到bucket
        print("上传到bucket")
        s3_client = boto3.client("s3")
        timestr = time.strftime('%Y-%m-%d-%H')
        s3_client.upload_file(dumpfile, self.bucket,
                              f"mtxdumps/dumps{timestr}.json")

    def backup_storage(self):
        print('backup_storage()')
        
    @atomic
    def handle(self, **options):
        print(settings.PROJECT_DIR)
        print(f'bucket_name: {self.bucket}')
        print("dump db")
        self.dump_db()
        self.backup_storage()

        print("finished !")
