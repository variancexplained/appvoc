#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/storage/review.py                                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 05:54:37 am                                                #
# Modified   : Saturday July 29th 2023 08:21:18 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

import pandas as pd
import numpy as np

from appstore.data.storage.base import Repo
from appstore.infrastructure.database.base import Database
from sqlalchemy.dialects.mysql import (
    LONGTEXT,
    BIGINT,
    VARCHAR,
    FLOAT,
)

# ------------------------------------------------------------------------------------------------ #
#                                    DATAFRAME DATA TYPES                                          #
# ------------------------------------------------------------------------------------------------ #
DATAFRAME_DTYPES = {
    "id": "string",
    "app_id": "string",
    "app_name": "string",
    "category_id": "category",
    "category": "category",
    "author": "string",
    "rating": np.float64,
    "title": "string",
    "content": "string",
    "vote_sum": np.int64,
    "vote_count": np.int64,
}


PARSE_DATES = {
    "date": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
}

# ------------------------------------------------------------------------------------------------ #
#                                      DATABASE DATA TYPES                                         #
# ------------------------------------------------------------------------------------------------ #
DATABASE_DTYPES = {
    "id": VARCHAR(64),
    "app_id": VARCHAR(24),
    "app_name": VARCHAR(128),
    "category_id": VARCHAR(8),
    "category": VARCHAR(128),
    "author": VARCHAR(128),
    "rating": FLOAT,
    "title": VARCHAR(256),
    "content": LONGTEXT,
    "vote_sum": BIGINT,
    "vote_count": BIGINT,
    "date": VARCHAR(32),
}


# ------------------------------------------------------------------------------------------------ #
class ReviewRepo(Repo):
    """Repository for reviews

    Args:
        database(Database): Database containing data to access.
    """

    __name = "review"

    def __init__(self, database: Database) -> None:
        super().__init__(name=self.__name, database=database)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def add(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data, tablename=self._name, dtype=DATABASE_DTYPES, if_exists="append"
        )
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def get(
        self, id: str, dtypes: dict = DATAFRAME_DTYPES, parse_dates: dict = None  # noqa
    ) -> pd.DataFrame:
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
            dtypes (dict): Dictionary mapping of column to data types
            parse_dates (dict): Dictionary of columns and keyword arguments for datetime parsing.
        """
        return super().get(id=id, dtypes=dtypes, parse_dates=parse_dates)

    def getall(self) -> pd.DataFrame:
        """Returns all data in the repository."""

        return super().getall(dtypes=DATAFRAME_DTYPES, parse_dates=PARSE_DATES)

    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data, tablename=self._name, dtype=DATABASE_DTYPES, if_exists="replace"
        )
        msg = f"Replace {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)

    @property
    def summary(self) -> pd.DataFrame:
        """Summarizes the app data by category"""
        df = self.getall()
        df2 = df.groupby(["category"])["id"].nunique().to_frame()
        df3 = df.groupby(["category"])["app_id"].nunique().to_frame()
        summary = df2.join(df3, on="category").reset_index()
        summary.columns = ["Category", "Reviews", "Apps"]
        return summary
