#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/repo/rating.py                                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 05:56:28 am                                                #
# Modified   : Sunday May 7th 2023 07:22:19 am                                                     #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
from datetime import datetime
import pandas as pd

import logging

from aimobile.data.repo import APPSTORE_RATING_DTYPES
from aimobile.data.repo.base import ARCHIVE, Repo
from aimobile.infrastructure.dal.base import Database
from aimobile.infrastructure.io.local import IOService


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
