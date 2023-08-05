import os
from time import time
from typing import Optional, TextIO

from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
import boto3
from pathlib import Path
import logging
import json
from datetime import datetime

from mtlibs.aws import s3_helper
logger = logging.getLogger(__name__)

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class Command(BaseCommand):

    help = """初始化云端核心部件"""

    def __init__(self) -> None:
        super().__init__(self)
        self.app_id = settings.MTX_APP_ID

    def create_bucket_static(self):
        """创建静态文件bucket"""

        bucket_name = f"{self.app_id}-static"
        print(f"静态文件bucket {bucket_name}")

        is_bucket_exists = s3_helper.bucket_exists(bucket_name)
        if not is_bucket_exists:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
            # cors 设置
            s3 = boto3.resource('s3')
            print("设置 bucket cors")
            bucket_cors = s3.BucketCors(bucket_name)
            response = bucket_cors.put(
                CORSConfiguration={
                    'CORSRules': [
                        {
                            # 'ID': 'xxxxxxff',
                            'AllowedHeaders': [
                                '*',
                            ],
                            'AllowedMethods': [
                                'GET',
                                'POST',
                                'HEAD',
                                'PUT',
                            ],
                            'AllowedOrigins': [
                                '*',
                                'http://*',
                                'https://*',
                            ],
                            'ExposeHeaders': [

                            ],
                            'MaxAgeSeconds': 3000
                        },
                    ]
                },
                # ChecksumAlgorithm='CRC32'|'CRC32C'|'SHA1'|'SHA256',
                # ExpectedBucketOwner='string'
            )
            policyJson = json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        # "Sid": "id-1",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": [
                            "s3:GetObject"
                        ],
                        "Resource": [
                            "arn:aws:s3:::"+bucket_name + "/*"
                        ]
                    },
                ]
            }, cls=SetEncoder)
        else:
            print("已经存在？")

    # def create_bucket_backup(self):
    #     """创建用于备份的s3 bucket"""

    #     bucket_name = f"{app_id}-backup"
    #     print(f"创建备份 bucket {bucket_name}")

    #     is_bucket_exists = s3_helper.bucket_exists(bucket_name)
    #     if not is_bucket_exists:
    #         s3_client = boto3.client('s3')
    #         s3_client.create_bucket(Bucket=bucket_name)
    #         # cors 设置
    #         s3 = boto3.resource('s3')
    #         print("设置 bucket cors")
    #         bucket_cors = s3.BucketCors(bucket_name)
    #         response = bucket_cors.put(
    #             CORSConfiguration={
    #                 'CORSRules': [
    #                     {
    #                         # 'ID': 'xxxxxxff',
    #                         'AllowedHeaders': [
    #                             '*',
    #                         ],
    #                         'AllowedMethods': [
    #                             'GET',
    #                             'POST',
    #                             'HEAD',
    #                             'PUT',
    #                         ],
    #                         'AllowedOrigins': [
    #                             '*',
    #                             'http://*',
    #                             'https://*',
    #                         ],
    #                         'ExposeHeaders': [

    #                         ],
    #                         'MaxAgeSeconds': 3000
    #                     },
    #                 ]
    #             },
    #             # ChecksumAlgorithm='CRC32'|'CRC32C'|'SHA1'|'SHA256',
    #             # ExpectedBucketOwner='string'
    #         )
    #     else:
    #         print("已经存在？")

    def create_bucket_storage(self):
        """创建 media bucket"""

        bucket_name = f"{self.app_id}-storage"
        print(f"create storage bucket {bucket_name}")

        is_bucket_exists = s3_helper.bucket_exists(bucket_name)
        if is_bucket_exists:
            print(f"skip for bucket exists '{bucket_name}' ")
        else:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
            # cors 设置
            s3 = boto3.resource('s3')
            print("设置 bucket cors")
            bucket_cors = s3.BucketCors(bucket_name)

            response = bucket_cors.put(
                CORSConfiguration={
                    'CORSRules': [
                        {
                            # 'ID': 'xxxxxxff',
                            'AllowedHeaders': [
                                '*',
                            ],
                            'AllowedMethods': [
                                'GET',
                                'POST',
                                'HEAD',
                                'PUT',
                            ],
                            'AllowedOrigins': [
                                '*',
                                'http://*',
                                'https://*',
                            ],
                            'ExposeHeaders': [

                            ],
                            'MaxAgeSeconds': 3000
                        },
                    ]
                },
                # ChecksumAlgorithm='CRC32'|'CRC32C'|'SHA1'|'SHA256',
                # ExpectedBucketOwner='string'
            )
            print(f'设置 {bucket_name} policy ')
            policyJson = json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        # "Sid": "id-1",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": [
                            "s3:GetObject",
                            "s3:PutObject",
                            "s3:PutObjectAcl"
                        ],
                        "Resource": [
                            "arn:aws:s3:::"+bucket_name + "/*"
                        ]
                    },
                ]
            }, cls=SetEncoder)

            response = s3_client.put_bucket_policy(
                Bucket=bucket_name,
                Policy=policyJson
            )

    def check_settings(self):
        """检测配置文件"""
        if settings.S3_BUCKET_STATIC != f"{self.app_id}-static":
            print(f"请将：S3_BUCKET_STATIC 设置为：{self.app_id}-static")
            return False
        if settings.AWS_STORAGE_BUCKET_NAME != f"{self.app_id}-storage":
            print(f"请将 AWS_STORAGE_BUCKET_NAME 设置为：{self.app_id}-storage")
            return False
        return True

    def save_meta(self):
        print("写入元数据到s3")
        meta = {
            'mtx_app_id': self.app_id,
            'latest_update': time()
        }
        s3_client = boto3.client('s3')
        bucket_name = f"{self.app_id}-storage"
        s3_helper.uploadFile_bytes(
            bucket=bucket_name,
            key='mtxmeta.json',
            bytes=json.dumps(meta, indent=4).encode(),
            s3_client=s3_client
        )

    def handle(self, **options):
        print("检查配置文件")
        if not self.check_settings():
            print("settings 设置不正确")
            return
        print("创建静态文件bucket")
        self.create_bucket_static()

        # print("create backup bucket")
        # self.create_bucket_backup()

        print("create storage bucket")
        self.create_bucket_storage()

        # print("执行命令： collectstatic --no-input -v 2")
        # call_command("collectstatic","--no-input", "-v","2")
        self.save_meta()
        print("finish !")
