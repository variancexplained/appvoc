#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/manage/base.py                                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday August 26th 2023 04:32:05 pm                                               #
# Modified   : Saturday August 26th 2023 04:52:05 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod


# ------------------------------------------------------------------------------------------------ #
class StorageManager(ABC):
    @property
    def database_backup_folder(self) -> str:
        """Returns the folder used to store database backkups."""
        return self._database_backup_folder

    @property
    def archive_folder(self) -> str:
        """Returns the folder used to store archives."""
        return self._archive_folder

    @abstractmethod
    def backup(self) -> bool:
        """Backups database

        Returns boolean. True indicates operation was successful.

        """

    @abstractmethod
    def restore(self, filepath: str) -> bool:
        """Restores the database

        Args:
            filepath (str): The filepath for the database backup to restore.

        Returns boolean. True indicates operation was successful.
        """

    @abstractmethod
    def archive(self) -> bool:
        """Archives the datas the data package."""

    @abstractmethod
    def upload(self, filepath: str, *args, **kwargs) -> bool:
        """Uploads the file to the cloud service provider.

        Args:
            filepath (str): The path to the file to upload.
        """

    @abstractmethod
    def download(self, filepath: str, *args, **kwargs) -> bool:
        """Downloads a file from the cloud service provider.

        Args:
            filepath (str): The destination filepath

        """
