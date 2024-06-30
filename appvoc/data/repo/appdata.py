#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/data/repo/appdata.py                                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 05:52:50 am                                                #
# Modified   : Sunday June 30th 2024 02:01:37 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Repository Implementation Module"""
import logging

import numpy as np
import pandas as pd
from sqlalchemy.dialects.mysql import BIGINT, FLOAT, LONGTEXT, VARCHAR  # , TINYINT

from appvoc.data.dataset.app import AppDataDataset
from appvoc.data.entity.app import AppData
from appvoc.data.repo.base import Repo
from appvoc.infrastructure.database.base import Database
from appvoc.infrastructure.file.config import FileConfig

# ------------------------------------------------------------------------------------------------ #
#                                    DATAFRAME DATA TYPES                                          #
# ------------------------------------------------------------------------------------------------ #
DATAFRAME_DTYPES = {
    "id": "string",
    "name": "string",
    "description": "string",
    "category_id": "category",
    "category": "category",
    #  "free": bool,
    "price": np.float64,
    "developer_id": "string",
    "developer": "string",
    "rating": np.float64,
    "ratings": np.int64,
    #  "ratings_per_month": np.float64,
    #   "months_avail": np.float64,
}

PARSE_DATES = {
    "released": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
    # "extracted": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
}

# ------------------------------------------------------------------------------------------------ #
#                                      DATABASE DATA TYPES                                         #
# ------------------------------------------------------------------------------------------------ #
DATABASE_DTYPES = {
    "id": VARCHAR(24),
    "name": VARCHAR(1024),
    "description": LONGTEXT,
    "category_id": VARCHAR(8),
    "category": VARCHAR(128),
    # "free": TINYINT,
    "price": FLOAT,
    "developer_id": VARCHAR(24),
    "developer": VARCHAR(256),
    "rating": FLOAT,
    "ratings": BIGINT,
    # "ratings_per_month": FLOAT,
    # "months_avail": FLOAT,
    "released": VARCHAR(32),
    # "extracted": VARCHAR(32),
}


# ------------------------------------------------------------------------------------------------ #
class AppDataRepo(Repo):
    """Repository for App Data

    Args:
        database(Database): Database containing data to access.
    """

    __name = "app"

    def __init__(self, database: Database, config=FileConfig) -> None:
        super().__init__(name=self.__name, database=database, config=config)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def summary(self) -> None:
        """Summarizes the data"""
        df = self.getall()

        summary = df["category"].value_counts().reset_index()
        summary.columns = ["category", "Examples"]
        df2 = df.groupby(by="category")["id"].nunique().to_frame()
        df3 = df.groupby(by="category")["rating"].mean().to_frame()
        df4 = df.groupby(by="category")["ratings"].sum().to_frame()

        summary = summary.join(df2, on="category")
        summary = summary.join(df3, on="category")
        summary = summary.join(df4, on="category")
        summary.columns = [
            "Category",
            "Examples",
            "Apps",
            "Average Rating",
            "Rating Count",
        ]
        return summary

    def load(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data, tablename=self._name, dtype=DATABASE_DTYPES, if_exists="append"
        )
        self.save()
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def get(
        self,
        id: str,  # noqa
        dtypes: dict = DATAFRAME_DTYPES,
        parse_dates: dict = PARSE_DATES,  # noqa
    ) -> AppData:
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
            dtypes (dict): Dictionary mapping of column to data types
            parse_dates (dict): Dictionary of columns and keyword arguments for datetime parsing.
        """
        df = super().get(id=id, dtypes=dtypes, parse_dates=parse_dates)
        if len(df) > 0:
            return AppData.from_df(df=df)
        else:
            return None

    def getall(self) -> pd.DataFrame:
        """Returns all data in the repository."""

        return super().getall(dtypes=DATAFRAME_DTYPES, parse_dates=PARSE_DATES)

    def get_ids(self, category_id: str) -> list:
        """Returns the list of app ids for the category

        Args:
            category_id (str): The four character AppVoC category identifier.
        """
        query = f"SELECT id FROM {self._name} WHERE category_id = :category_id;"
        params = {"category_id": category_id}
        ids = self._database.query(query=query, params=params)
        return list(ids["id"].values)

    def get_dataset(self) -> AppDataDataset:
        df = self.getall()
        return AppDataDataset(df=df)

    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data, tablename=self._name, dtype=DATABASE_DTYPES, if_exists="replace"
        )
        self.save()
        msg = f"Replaced {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)
