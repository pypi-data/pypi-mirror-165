import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
import boto3
from pathlib import Path
import logging

from mtlibs.aws import s3_helper
logger = logging.getLogger(__name__)

class Command(BaseCommand):  
    help = """部署静态文件到云端(s3)"""

    # def create_static_file_bucket(self):
    #     """创建静态文件bucket"""

    #     bucket_name = settings.S3_BUCKET_STATIC
    #     print(f"静态文件bucket {bucket_name}")

    #     is_bucket_exists = s3_helper.bucket_exists(bucket_name)
    #     if not is_bucket_exists:
    #         print('请运行命令：mtx_init_cloud 初始化相关基础设施')
    #         return
            


    def handle(self, **options):
        print("设置bucket")
       
        bucket_name = settings.S3_BUCKET_STATIC
        print(f"静态文件bucket {bucket_name}")

        is_bucket_exists = s3_helper.bucket_exists(bucket_name)
        if not is_bucket_exists:
            print('请运行命令：mtx_init_cloud 初始化相关基础设施')
            return
        
        print("执行命令： collectstatic --no-input -v 2")
        call_command("collectstatic","--no-input" , "-v","2")
        print("finish !")
