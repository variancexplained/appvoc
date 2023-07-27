#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/storage/appdata.py                                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 05:52:50 am                                                #
# Modified   : Wednesday July 26th 2023 12:04:28 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Repository Implementation Module"""
import os
from datetime import datetime
import logging

import numpy as np
import pandas as pd

from appstore.data.storage import APPSTORE_APPDATA_DTYPES
from appstore.data.storage.base import ARCHIVE, Repo
from appstore.infrastructure.database.base import Database
from appstore.infrastructure.io.local import IOService

# ------------------------------------------------------------------------------------------------ #
#                                    PANDAS DATA TYPES                                             #
# ------------------------------------------------------------------------------------------------ #
DTYPES = {
    "id": "string",
    "name": "string",
    "description": "string",
    "category_id": "category",
    "category": "category",
    "price": np.float64,
    "developer_id": "string",
    "developer": "string",
    "rating": np.float64,
    "ratings": np.int64,
}

PARSE_DATES = {
    "released": {"errors": "ignore", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
}


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
        self._df = None
        self._database.insert(
            data=data, tablename=self._name, dtype=APPSTORE_APPDATA_DTYPES, if_exists="append"
        )
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def getall(self) -> pd.DataFrame:
        """Returns all data in the repository."""

        return super().getall(parse_dates=PARSE_DATES)

    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._df = None
        self._database.insert(
            data=data, tablename=self._name, dtype=APPSTORE_APPDATA_DTYPES, if_exists="replace"
        )
        msg = f"Replaced {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)

    def update(self, id: int, keys: list, values: list) -> None:
        """Updates the keys with the values for the app designated by the id.

        Args:
            id (int): The app id
            keys (str): A list of keys corresponding to columns on the database.
            values (str): A list of values for the corresponding keys.
        """
        self._df = None
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

    def export(self, directory: str = ARCHIVE["appstore"]) -> None:
        os.makedirs(directory, exist_ok=True)
        filename = "appdata_" + datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + ".pkl"
        filepath = os.path.join(directory, filename)
        IOService.write(filepath=filepath, data=self.getall())
