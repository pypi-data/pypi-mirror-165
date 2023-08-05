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
from pathlib import Path
app_id = settings.MTX_APP_ID


class Command(BaseCommand):

    help = '基于 s3 的storage 管理，包括下载备份，上传还原'
    
    def __init__(self):
        self.bucket = f"{app_id}-storage"
        self.s3_client = boto3.client('s3')
        self.local_storage_dir = os.path.join(settings.PROJECT_DIR, '.storage')

    def add_arguments(self, parser):
        # parser.add_argument('direction', type=str)
        parser.add_argument(
            '--up',
            # nargs='?',
            # action='store_const',
            default='down',
            help='--up=up 为上传，否则为下载',
        )
        
    def download(self):
        Path(self.local_storage_dir).parent.mkdir(exist_ok=True)
        s3_helper.download_dir(prefix='',
                               local=self.local_storage_dir, 
                               bucket=self.bucket,
                               client=self.s3_client
                               )
    def upload(self):
        print("upload")        
        session = boto3.Session()
        s3_helper.upload_dir(
            dir=self.local_storage_dir,
            bucket=self.bucket,
            prefix='laji/',
            session=session,
        )
        
        
    def handle(self, *args, **options):
        print(
            f'project dir: {settings.PROJECT_DIR}, bucket_name: {self.bucket}')
        
        if options['up'] == 'down':
            self.download()
        else:
            self.upload()

        print('finished !')
