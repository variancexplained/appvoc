#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/storage/manager.py                                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday August 26th 2023 04:52:34 pm                                               #
# Modified   : Sunday August 27th 2023 06:36:05 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
import logging
import shutil

from dependency_injector.wiring import inject, Provide

from appstore.container import AppstoreContainer
from appstore.data.repo.uow import UoW
from appstore.data.storage.base import StorageManager
from appstore.infrastructure.cloud.amazon import AWS
from appstore.infrastructure.file.archive import FileArchiver
from appstore.infrastructure.database.base import Database
from appstore.infrastructure.file.io import IOService


# ------------------------------------------------------------------------------------------------ #
class DataStorageManager(StorageManager):
    @inject
    def __init__(
        self,
        archiver: FileArchiver = Provide[AppstoreContainer.file.archiver],
        cloud: AWS = Provide[AppstoreContainer.cloud.aws],
        database: Database = Provide[AppstoreContainer.data.db],
        uow: UoW = Provide[AppstoreContainer.data.uow],
    ) -> None:
        self._archiver = archiver
        self._cloud = cloud
        self._database = database
        self._uow = uow

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def archiver(self) -> FileArchiver:
        """Returns the file archiver"""
        return self._archiver

    @property
    def database(self) -> Database:
        """Returns the database"""
        return self._database

    @property
    def cloud(self) -> AWS:
        """ "Returns the AWS instance"""
        return self._cloud

    @property
    def uow(self) -> UoW:
        """Returns the Unit of Work Repositories."""
        return self._uow

    def backup(self) -> str:
        """Performs a backup of the database"""
        filepath = self._database.backup()
        msg = f"Backed up database to {filepath}"
        self._logger.info(msg)
        return filepath

    def restore(self, filepath: str) -> None:
        """Performs a database restore

        Args:
            filepath (str): The filepath from which the database will be restored
        """
        self._database.restore(filepath=filepath)
        self._database.commit()
        msg = f"Restored database from {filepath}"
        self._logger.info(msg)

    def purge(self) -> None:
        """Purges the data in the database, but keeps the tables."""
        if self._database.mode == "test":
            self._uow.appdata_repo.delete_all()
            self._uow.save()
            self._uow.rating_repo.delete_all()
            self._uow.save()
            self._uow.review_repo.delete_all()
            self._uow.save()

        else:
            msg = "Purge is not allowed in production mode."
            self._logger.info(msg)

    def archive(self) -> str:
        """Archives the data into a single tar.gz file and uploads it to the cloud

        Returns the filepath of the archive.
        """
        # Create a fresh archive directory
        shutil.rmtree(self._archiver.staging_folder, ignore_errors=True)
        os.makedirs(self._archiver.staging_folder, exist_ok=True)
        # Export the data into the archive folder
        self._export()
        # Call the Archiver to create the archive
        return self._archiver.archive()

    def recover(self, filepath: str) -> None:
        """Extracts an archive into the staging area and imports the data into the repository.

        Args:
            filepath (str): Archive filepath.
        """
        self._archiver.extract(filepath=filepath)
        for filename in os.listdir(self._archiver.staging_folder):
            filepath = os.path.join(self._archiver.staging_folder, filename)
            df = IOService.read(filepath)
            if "appdata" in filename:
                self._uow.appdata_repo.load(data=df)
                self._uow.save()
            elif "rating" in filename:
                self._uow.rating_repo.load(data=df)
                self._uow.save()
            else:
                self._uow.review_repo.load(data=df)
                self._uow.save()

        shutil.rmtree(self._archiver.staging_folder)

    def upload(self, filepath: str) -> None:
        """Uploads the archive to the designated cloud provider

        Args:
            filepath (str): The path to the file to be uploaded.
        """
        self._cloud.upload(filepath=filepath)

    def exists(self, object_name: str) -> bool:
        """Uploads the archive to the designated cloud provider

        Args:
            object_name (str): Name of object on cloud servers
            bucket (str): Name of bucket on the server.
        """
        return self._cloud.exists(object_name=object_name)

    def download(self, filepath: str, object_name) -> None:
        """Uploads the archive to the designated cloud provider

        Args:
            filepath (str): Path to the file to be downloaded
            object_name (str): Name of object in the cloud service
        """
        self._cloud.download(filepath=filepath, object_name=object_name)

    def _export(self) -> None:
        # Export appstore data
        self._uow.appdata_repo.export(
            directory=self._archiver.staging_folder,
            format="csv",
            by_category=False,
            with_datetime=False,
        )
        # Export rating data
        self._uow.rating_repo.export(
            directory=self._archiver.staging_folder,
            format="csv",
            by_category=False,
            with_datetime=False,
        )
        # Export review data by category
        self._uow.review_repo.export(
            directory=self._archiver.staging_folder,
            format="tsv",
            by_category=True,
            with_datetime=False,
        )
