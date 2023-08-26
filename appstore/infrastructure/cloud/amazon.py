#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/infrastructure/cloud/amazon.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday August 24th 2023 06:15:57 pm                                               #
# Modified   : Friday August 25th 2023 11:23:44 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging
import boto3
from botocore.exceptions import ClientError
import os

from appstore.data.manage.base import CloudStorageManager

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------------ #
class AWS(CloudStorageManager):
    """AWS S3 Storage Manager"""

    def __init__(self, default_bucket: str = None) -> None:
        super().__init__()
        self._default_bucket = default_bucket

    def upload(self, filepath: str, bucket: str = None, object_name: str = None) -> bool:
        """Uploads a file to an S3 Bucket

        Args:
            filepath (str): Path to file to upload
            bucket (str): Bucket into which, data will be uploaded. If not specified
                the default bucket will be used.
            object_name (str) S3 Object name. If not provided, then the basename from
                the filepath will be used.

        Returns boolean: True if successful, False if not.
        """
        bucket = bucket or self._default_bucket

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(filepath)

        # Upload the file
        s3_client = boto3.client("s3")
        try:
            response = s3_client.upload_file(Filename=filepath, Bucket=bucket, Key=object_name)
        except ClientError as e:  # pragma: no cover
            logger.exception(f"Client exception occurred.\n{response}\n{e}")  # noqa

    def download(
        self,
        filepath: str,
        object_name: str,
        bucket: str = None,
    ) -> bool:
        """Downloads a file from an S3 bucket

        Args:
            filepath (str): Path to file to upload
            object_name (str) S3 Object name.
            bucket (str): Bucket from which the file will be downloaded.
                If not specified, the default bucket will be used.

        Returns boolean: True if successful, False if not.
        """
        bucket = bucket or self._default_bucket

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        s3_client = boto3.client("s3")
        try:
            s3_client.download_file(Bucket=bucket, Key=object_name, Filename=filepath)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                logger.info(f"Object {object_name} does not exist in {bucket}")  # noqa
            else:  # pragma: no cover
                logger.exception(f"Client exception occurred.\n{e}")  # noqa
            return False
        return True

    def exists(self, object_name: str, bucket: str = None) -> bool:
        """Evaluates the existence of an object in the S3 bucket.

        Args:
            object_name (str): Name of the object.
            bucket (str): S3 Bucket. If not provided, the default bucket will be used.

        """
        bucket = bucket or self._default_bucket

        s3_client = boto3.client("s3")
        try:
            s3_client.head_object(Bucket=bucket, Key=object_name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                logger.info(f"Object {object_name} does not exist in {bucket}")  # noqa
            else:  # pragma: no cover
                logger.exception(f"Client exception occurred.\n{e}")  # noqa
            return False
        return True

    def remove(self, object_name: str, bucket: str = None) -> bool:
        """Evaluates the existence of an object in the S3 bucket.

        Args:
            object_name (str): Name of the object.
            bucket (str): S3 Bucket. If not provided, the default bucket will be used.

        """
        bucket = bucket or self._default_bucket

        s3_client = boto3.client("s3")
        try:
            s3_client.delete_object(Bucket=bucket, Key=object_name)
        except ClientError as e:  # pragma: no cover
            logger.exception(f"Client exception occurred.\n{e}")  # noqa
            return False
        return True
