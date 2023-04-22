#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/infrastructure/dal/repo.py                                                #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday April 18th 2023 05:37:06 pm                                                 #
# Modified   : Saturday April 22nd 2023 02:17:21 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Repository Implementation Module"""
import os
from datetime import datetime
import pandas as pd
from sqlalchemy.dialects.mysql import (
    MEDIUMTEXT,
    LONGTEXT,
    BIGINT,
    VARCHAR,
    INTEGER,
    FLOAT,
)
import logging

from aimobile.domain.repo import Repo
from aimobile.infrastructure.dal.base import Database, ARCHIVE
from aimobile.infrastructure.io.local import IOService


# ------------------------------------------------------------------------------------------------ #
class AppDataRepo(Repo):
    """Repository for App Data

    Args:
        database(Database): Database containing data to access.
    """

    __name = "appdata"

    def __init__(self, database: Database) -> None:
        super().__init__(name=self.__name, database=database)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def add(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        dtype = {
            "id": BIGINT,
            "name": VARCHAR(256),
            "description": MEDIUMTEXT,
            "category_id": INTEGER,
            "category": VARCHAR(128),
            "price": FLOAT,
            "developer_id": BIGINT,
            "developer": VARCHAR(256),
            "rating": FLOAT,
            "ratings": BIGINT,
            "released": VARCHAR(32),
            "source": VARCHAR(128),
        }
        self._database.insert(data=data, tablename=self._name, dtype=dtype, if_exists="append")
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def update_app(self, id: int, keys: list, values: list) -> None:
        """Updates the keys with the values for the app designated by the id.

        Args:
            id (int): The app id
            keys (str): A list of keys corresponding to columns on the database.
            values (str): A list of values for the corresponding keys.
        """
        kv = ""
        for i, key in enumerate(keys):
            if i == 0:
                kv += f"appdata.{key} = :{key}"
            else:
                kv += f", appdata.{key} = :{key}"

        query = f"UPDATE appdata SET {kv} WHERE appdata.id = :id;"
        params = {k: v for (k, v) in zip(keys, values)}
        params["id"] = id
        self._database.execute(query=query, params=params)

    def summarize(self) -> pd.DataFrame:
        """Summarizes the app data by category"""
        df = self.getall()
        counts = df["category"].value_counts().reset_index()
        total_rating_counts = df[["category", "ratings"]].groupby(by=["category"]).sum()
        rating_data = df[["category", "rating", "ratings"]].groupby(by=["category"]).mean()
        summary = counts.join(rating_data, on="category", how="left")
        summary = summary.join(total_rating_counts, on="category", rsuffix="total", how="left")
        summary.columns = [
            "Category",
            "App Count",
            "Average Rating",
            "Average Rating Count",
            "Total Rating Count",
        ]
        return summary

    def export(self, directory: str = ARCHIVE["appstore"]) -> None:
        os.makedirs(directory, exist_ok=True)
        filename = "appdata_" + datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + ".pkl"
        filepath = os.path.join(directory, filename)
        IOService.write(filepath=filepath, data=self.getall())


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
        dtype = {
            "id": BIGINT,
            "app_id": BIGINT,
            "app_name": VARCHAR(128),
            "category_id": INTEGER,
            "category": VARCHAR(128),
            "author": VARCHAR(128),
            "rating": FLOAT,
            "title": VARCHAR(256),
            "content": LONGTEXT,
            "vote_sum": BIGINT,
            "vote_count": BIGINT,
            "date": VARCHAR(32),
            "source": VARCHAR(128),
        }
        self._database.insert(data=data, tablename=self._name, dtype=dtype, if_exists="append")
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def summarize(self) -> pd.DataFrame:
        """Summarizes the app data by category"""
        df = self.getall()
        summary = df["category"].value_counts().reset_index()
        df2 = df.groupby(by="category")["app_id"].nunique().to_frame()
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
