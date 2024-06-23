#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/data/storage/base.py                                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday August 27th 2023 03:39:38 am                                                 #
# Modified   : Sunday August 27th 2023 04:12:30 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod, abstractproperty

from appvoc.data.repo.uow import UoW
from appvoc.infrastructure.cloud.amazon import AWS
from appvoc.infrastructure.file.archive import FileArchiver
from appvoc.infrastructure.database.base import Database

# ------------------------------------------------------------------------------------------------ #


class StorageManager(ABC):
    @abstractproperty
    def archiver(self) -> FileArchiver:
        """Returns the file archiver"""

    @abstractproperty
    def database(self) -> Database:
        """Returns the database"""

    @abstractproperty
    def cloud(self) -> AWS:
        """ "Returns the cloud management instance"""

    @abstractproperty
    def uow(self) -> UoW:
        """Returns the Unit of Work Repositories."""

    @abstractmethod
    def backup(self) -> None:
        """Performs a backup of the database"""

    @abstractmethod
    def restore(self, filepath: str) -> None:
        """Restores the database from file"""

    @abstractmethod
    def archive(self) -> None:
        """Creates an archive of the data"""

    @abstractmethod
    def upload(self, filepath: str) -> None:
        """Uploads the data to the cloud service provider"""

    @abstractmethod
    def download(self, filepath: str, object_name: str) -> None:
        """Downloads an object from the cloud service provider"""
