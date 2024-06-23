#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/infrastructure/cloud/amazon.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday August 24th 2023 06:15:57 pm                                               #
# Modified   : Sunday August 27th 2023 04:22:54 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging
import boto3
from botocore.exceptions import ClientError
import os

from appvoc.infrastructure.cloud.config import CloudConfig
from appvoc.infrastructure.cloud.base import CloudStorageManager


# ------------------------------------------------------------------------------------------------ #
class AWS(CloudStorageManager):
    """AWS S3 Storage Manager"""

    def __init__(self, config: CloudConfig) -> None:
        super().__init__()
        self._config = config()
        self._default_bucket = self._config.bucket
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def upload(
        self, filepath: str, bucket: str = None, object_name: str = None
    ) -> None:
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
            response = s3_client.upload_file(
                Filename=filepath, Bucket=bucket, Key=object_name
            )
        except ClientError as e:  # pragma: no cover
            self._logger.exception(
                f"Client exception occurred.\n{response}\n{e}"
            )  # noqa
            raise
        else:
            msg = f"Uploaded {filepath} to {bucket}"
            self._logger.info(msg)

    def download(
        self,
        filepath: str,
        object_name: str,
        bucket: str = None,
    ) -> None:
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
                self._logger.info(
                    f"Object {object_name} does not exist in {bucket}"
                )  # noqa
            else:  # pragma: no cover
                self._logger.exception(f"Client exception occurred.\n{e}")  # noqa
            raise
        else:
            msg = f"Downloaded {object_name} to {filepath}"
            self._logger.info(msg)

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
                self._logger.info(
                    f"Object {object_name} does not exist in {bucket}"
                )  # noqa
            else:  # pragma: no cover
                self._logger.exception(f"Client exception occurred.\n{e}")  # noqa
            return False
        else:
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
            self._logger.exception(f"Client exception occurred.\n{e}")  # noqa
            raise
        else:
            msg = f"Removed {object_name} from S3 bucket {bucket}"
            self._logger.info(msg)
