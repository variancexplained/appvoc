#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/appstore/repo.py                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday April 18th 2023 05:37:06 pm                                                 #
# Modified   : Thursday April 20th 2023 12:02:34 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Data Access Layer Moddule"""
import pandas as pd
from typing import Union

from aimobile.domain.repo import RepoABC
from aimobile.infrastructure.dal.base import Database


# ------------------------------------------------------------------------------------------------ #
class Repo(RepoABC):
    """Provides a generic data access layer

    Args:
        database(Database): Database containing data to access.
    """

    def __init__(self, database: Database) -> None:
        self._database = database

    def add(self, data: pd.DataFrame, tablename: str) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
            tablename (str): Table to which the data must be added.
        """
        self._database.insert(data=data, tablename=tablename)

    def get(self, tablename: str, id: Union[str, int]) -> pd.DataFrame:
        """Returns all data in the designated table in DataFrame format.

        Args:
            id (Union[str,int]): App id.
            tablename (str): The table from which the data is to be obtained.
        """
        query = f"SELECT * FROM {tablename} WHERE id = :id;"
        params = {"id": id}
        with self._database as database:
            df = database.query(query=query, params=params)
        return df

    def get_by_category(self, category_id: Union[str, int], tablename: str) -> pd.DataFrame:
        """Obtains data from the given table by category id

        Args:
            category_id (Union[str,int]): The mobile app category.
            tablename (str): An existing table in the database.
        """
        query = f"SELECT * FROM {tablename} WHERE category_id = :category_id;"
        params = {"category_id": category_id}
        with self._database as database:
            df = database.query(query=query, params=params)
        return df

    def exists(self, id: Union[str, int], tablename: str = "appdata") -> bool:
        """Assesses the existence of an app in the database.

        Args:
            id (Union[str,int]): The app id.
            tablename (str): The 'appdata' table.
        """
        query = f"SELECT EXISTS(SELECT 1 FROM {tablename} id = :id);"
        params = {"id": id}
        with self._database as database:
            return database.exists(query=query, params=params)

    def count(self, tablename: str, id: Union[str, int] = None) -> int:
        """Counts the rows matching the criteria. Counts all rows if id is None.

        Args:
            tablename (str): The name of the table
            id (Union[str,int]): The app id

        Returns number of rows matching criteria
        """
        if id is not None:
            query = f"SELECT * FROM {tablename} WHERE id = :id;"
            params = {"id": id}
        else:
            query = f"SELECT * FROM {tablename};"
            params = {}

        df = self._database.query(query=query, params=params)
        return df.shape[0]

    def delete(self, tablename: str, id: Union[str, int] = None) -> int:
        """Deletes the row designated by the tablename an id. Deletes all rows if id is None

        Args:
            tablename (str): The name of the table
            id (Union[str,int]): The app id

        Returns number of rows deleted.
        """
        if id is not None:
            query = f"DELETE FROM {tablename} WHERE id = :id;"
            params = {"id": id}
        else:
            query = f"DELETE FROM {tablename};"
            params = {}

        self._database.delete(query=query, params=params)

    def save(self) -> None:
        """Saves changes to the underlying database"""
        self._database.commit()
