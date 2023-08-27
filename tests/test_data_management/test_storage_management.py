#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /tests/test_data_management/test_storage_management.py                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday August 26th 2023 10:20:27 pm                                               #
# Modified   : Sunday August 27th 2023 06:32:17 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
import inspect
from datetime import datetime
import pytest
import logging

from appstore.data.storage.manager import DataStorageManager


# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"

ARCHIVE = None
DIRECTORY = "tests/data/manage"
OBJECT_NAME = "credit_score_dataset.csv"


@pytest.mark.dm
class TestDataStorageManager:  # pragma: no cover
    # ============================================================================================ #
    def test_backup_restore(self, container, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        ds = DataStorageManager()
        filepath = ds.backup()
        assert os.path.exists(filepath)
        # Purge
        ds.purge()
        # Restore
        ds.restore(filepath=filepath)
        #  Validate data appdata
        repo = container.data.appdata_repo()
        df = repo.getall()
        assert df.shape[0] == 100

        #  Validate rating data
        repo = container.data.rating_repo()
        df = repo.getall()
        assert df.shape[0] == 100

        #  Validate review data
        repo = container.data.review_repo()
        df = repo.getall()
        assert df.shape[0] == 100

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_archive(self, container, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        ds = DataStorageManager()
        archive = ds.archive()
        assert os.path.exists(archive)

        # Upload the archive
        ds.upload(filepath=archive)
        object_name = os.path.basename(archive)
        assert ds.exists(object_name=object_name)

        # Purge the data
        ds.purge()

        # Recovery the data from an archive
        filepath = "tests/data/backup/archive/appstore_2023-08-27_T063129.tar.gz"
        ds.recover(filepath=filepath)

        #  Validate data appdata
        repo = container.data.appdata_repo()
        df = repo.getall()
        assert df.shape[0] == 100

        #  Validate rating data
        repo = container.data.rating_repo()
        df = repo.getall()
        assert df.shape[0] == 100

        #  Validate review data
        repo = container.data.review_repo()
        df = repo.getall()
        assert df.shape[0] == 100

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_download(self, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        ds = DataStorageManager()
        filepath = "tests/data/archive/credit_score_dataset.csv"
        object_name = "credit_score_dataset.csv"
        ds.download(filepath, object_name=object_name)
        assert os.path.exists(filepath)
        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)
