#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/infrastructure/file/archive.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday August 26th 2023 04:52:34 pm                                               #
# Modified   : Sunday August 27th 2023 06:09:21 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import tarfile
import shutil

from appstore.infrastructure.file.base import Archiver
from appstore.infrastructure.file.config import FileConfig

# ------------------------------------------------------------------------------------------------ #
load_dotenv()


# ------------------------------------------------------------------------------------------------ #
class FileArchiver(Archiver):
    def __init__(self, config: FileConfig = FileConfig) -> None:
        self._config = config()
        self._archive_folder = self._config.archive
        self._staging_folder = self._config.staging
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def archive_folder(self) -> str:
        return self._archive_folder

    @property
    def staging_folder(self) -> str:
        return self._staging_folder

    def archive(self) -> str:
        """Archives the data into a single tar.gz file and uploads it to the cloud

        Returns the filepath of the archive.
        """
        # Create archive filepath
        filepath = self._get_archive_filename()
        # Create archive
        try:
            with tarfile.open(filepath, "w:gz") as tar:
                for filename in os.listdir(self.staging_folder):
                    path = os.path.join(self.staging_folder, filename)
                    tar.add(path, arcname=filename)
        except FileExistsError:
            msg = f"File {filepath} already exists."
            self._logger.exception(msg)
            raise
        except tarfile.ReadError:  # pragma: no cover
            msg = f"Tarfile {filepath} is open or somehow invalid."
            self._logger.exception(msg)
            raise
        except tarfile.CompressionError:  # pragma: no cover
            msg = f"Tarfile {filepath} cannot be decoded or compression method is not supported."
            self._logger.exception(msg)
            raise
        except tarfile.TarError:  # pragma: no cover
            msg = f"Tarfile exception occurred with file {filepath}."
            self._logger.exception(msg)
            raise
        else:
            msg = f"Archived the database to {filepath}"
            self._logger.info(msg)
            archive_filepath = os.path.join(self._archive_folder, os.path.basename(filepath))
            shutil.move(filepath, archive_filepath)
            msg = "Moved the archive out of the staging area."
            self._logger.info(msg)
            shutil.rmtree(self._staging_folder, ignore_errors=True)
            msg = "Purged staging area"
            self._logger.info(msg)
            return archive_filepath

    def extract(self, filepath: str) -> None:
        """Extracts an archive into the staging area

        Args:
            filepath (str): Archive filepath.
        """
        with tarfile.open(filepath) as tar:
            tar.extractall(self._staging_folder)

    def _get_archive_filename(self) -> str:
        filename = "appstore_" + datetime.now().strftime("%Y-%m-%d_T%H%M%S") + ".tar.gz"
        filepath = os.path.join(self.staging_folder, filename)
        return os.path.abspath(filepath)
