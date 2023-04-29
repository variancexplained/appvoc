#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/repo/appstore.py                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday April 18th 2023 05:37:06 pm                                                 #
# Modified   : Saturday April 29th 2023 06:34:39 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Repository Implementation Module"""
import os
from datetime import datetime
import pandas as pd

import logging

from aimobile.data.repo import (
    APPSTORE_APPDATA_DTYPES,
    APPSTORE_RATING_DTYPES,
    APPSTORE_REVIEW_DTYPES,
)
from aimobile.data.repo.base import ARCHIVE, Repo, UoW
from aimobile.infrastructure.dal.base import Database
from aimobile.infrastructure.io.local import IOService
from aimobile.data.repo.task import TaskRepo


# ------------------------------------------------------------------------------------------------ #
class AppStoreRatingRepo(Repo):
    """Repository for rating data

    Args:
        database(Database): Database containing data to access.
    """

    __name = "rating"

    def __init__(self, database: Database) -> None:
        super().__init__(name=self.__name, database=database)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def add(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._df = None
        self._database.insert(
            data=data, tablename=self._name, dtype=APPSTORE_RATING_DTYPES, if_exists="append"
        )
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._df = None
        self._database.insert(
            data=data, tablename=self._name, dtype=APPSTORE_RATING_DTYPES, if_exists="replace"
        )
        msg = f"Replace {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)

    @property
    def summary(self) -> pd.DataFrame:
        """Summarizes the app data by category"""
        df = self.getall()
        summary = df["category"].value_counts().reset_index()
        df2 = df.groupby(by="category")["id"].nunique().to_frame()
        df3 = df.groupby(by="category")["rating"].mean().to_frame()
        summary = summary.join(df2, on="category")
        summary = summary.join(df3, on="category")
        summary.columns = ["Category", "Reviews", "Apps", "Average Rating"]
        return summary

    def export(self, directory: str = ARCHIVE["appstore"]) -> None:
        os.makedirs(directory, exist_ok=True)
        filename = "reviews_" + datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + ".pkl"
        filepath = os.path.join(directory, filename)
        IOService.write(filepath=filepath, data=self.getall())


# ------------------------------------------------------------------------------------------------ #
#                              APPSTORE UNIT OF WORK CLASS                                         #
# ------------------------------------------------------------------------------------------------ #
class AppStoreUoW(UoW):
    """Appstore Unit of Work

    This Unit of Work class has the sole responsibility of ensuring that all appstore repositories
    share the same database context.
    Args:
        appdata_repository (type[AppStoreAppDataRepo]): A Repo class type
        review_repository (type[AppStoreReviewRepo]): A Repo class type
        rating_respository (type[AppStoreRatingRepo]): A AppStoreRatingRepo class type
        database (Database): A Database instance from the dependency injector container.

    """

    def __init__(
        self,
        database: Database,
        appdata_repository: type[Repo] = AppStoreAppDataRepo,
        review_repository: type[Repo] = AppStoreReviewRepo,
        rating_repository: type[Repo] = AppStoreRatingRepo,
        task_repository: type[Repo] = TaskRepo,
    ) -> None:
        super().__init__(database=database)
        self._appdata_repository = appdata_repository
        self._review_repository = review_repository
        self._rating_repository = rating_repository
        self._task_repository = task_repository

    @property
    def appdata_repository(self) -> Repo:
        """Returns a appdata repository instantiated with the database context."""
        return self._appdata_repository(database=self._database)

    @property
    def review_repository(self) -> Repo:
        """Returns a review repository instantiated with the database context."""
        return self._review_repository(database=self._database)

    @property
    def rating_repository(self) -> Repo:
        """Returns a rating repository instantiated with the database context."""
        return self._rating_repository(database=self._database)

    @property
    def task_repository(self) -> Repo:
        """Returns a rating repository instantiated with the database context."""
        return self._task_repository(database=self._database)
