#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/manage/storage.py                                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday August 26th 2023 04:52:34 pm                                               #
# Modified   : Saturday August 26th 2023 06:06:31 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
from dotenv import load_dotenv

from dependency_injector.wiring import inject, Provide

from appstore.data.manage.base import StorageManager
from appstore.infrastructure.cloud.amazon import AWS

# ------------------------------------------------------------------------------------------------ #
load_dotenv()


# ------------------------------------------------------------------------------------------------ #
class DataStorageManager(StorageManager):
    def __init__(
        self,
        cloud: type(AWS) = AWS,
    ) -> None:
        bucket = os.getenv("AWS_BUCKET")
        self._cloud = cloud(default_bucket=bucket)
        self._database_backup_folder = os.getenv("DATABASE_BACKUP_FOLDER")
        self._archive_folder = os.getenv("ARCHIVE_FOLDER")
