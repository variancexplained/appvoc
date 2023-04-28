#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/infrastructure/repo/base.py                                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 11:34:11 am                                                  #
# Modified   : Friday April 28th 2023 02:04:37 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module provides basic database interface"""
from __future__ import annotations
from abc import ABC, abstractmethod
import logging
from typing import Union

import pandas as pd

from aimobile.infrastructure.dal.base import Database

# ------------------------------------------------------------------------------------------------ #
ARCHIVE = {"appstore": "data/appstore/archive", "googleplay": "data/googleplay/archive"}


# ------------------------------------------------------------------------------------------------ #
class Repo(ABC):
    """Provides base class for all repositories classes.

    Args:
        name (str): Repository name. This will be the name of the underlying database table.
        database(Database): Database containing data to access.
    """

    def __init__(self, name: str, database: Database) -> None:
        self._name = name
        self._database = database
        self._df = None

    @abstractmethod
    def add(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """

    @abstractmethod
    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """

    def info(self) -> pd.DataFrame:
        """Returns a DataFrame containing a basic summary of the data.

        Returns a DataFrame containing:
            - column names
            - data types
            - size (Bytes)
            - variable type
            - cardinality
        """
        df = self.getall()

        df1 = df.dtypes.to_frame()
        df2 = df.count().to_frame()
        df3 = df.memory_usage(index=False, deep=True).to_frame()
        df4 = df.nunique().to_frame()
        info = pd.concat([df1, df2, df3, df4], axis=1)
        info.columns = ["Dtype", "Non-Null Count", "Bytes", "Cardinality"]
        return info

    @property
    @abstractmethod
    def summary(self) -> pd.DataFrame:
        """Returns a summary of the repository in DataFrame format"""

    def get(self, id: Union[str, int]) -> pd.DataFrame:
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
        """
        query = f"SELECT * FROM {self._name} WHERE id = :id;"
        params = {"id": id}
        return self._database.query(query=query, params=params)

    def get_by_category(self, category_id: Union[str, int]) -> pd.DataFrame:
        """Obtains data from the given table by category id

        Args:
            category_id (Union[str,int]): The mobile app category.
        """
        query = f"SELECT * FROM {self._name} WHERE category_id = :category_id;"
        params = {"category_id": category_id}
        return self._database.query(query=query, params=params)

    def getall(self) -> pd.DataFrame:
        """Returns all data in the repository."""
        if self._df is not None:
            return self._df
        else:
            query = f"SELECT * FROM {self._name};"
            params = None
            self._df = self._database.query(query=query, params=params)
            return self._df

    def exists(self, id: Union[str, int] = "appdata") -> bool:
        """Assesses the existence of an entity in the database.

        Args:
            id (Union[str,int]): The app id.
        """
        query = f"SELECT EXISTS(SELECT 1 FROM {self._name} WHERE id = :id);"
        params = {"id": id}
        return self._database.exists(query=query, params=params)

    def count(self, id: Union[str, int] = None) -> int:
        """Counts the entities matching the criteria. Counts all entities if id is None.

        Args:
            id (Union[str,int]): Entity id

        Returns number of rows matching criteria
        """
        if id is not None:
            query = f"SELECT * FROM {self._name} WHERE id = :id;"
            params = {"id": id}
        else:
            query = f"SELECT * FROM {self._name};"
            params = {}

        df = self._database.query(query=query, params=params)
        return df.shape[0]

    def delete(self, id: Union[str, int]) -> int:
        """Deletes the entity designated by the id.

        Args:
            id (Union[str,int]): Entity id

        """
        self._df = None
        query = f"DELETE FROM {self._name} WHERE id = :id;"
        params = {"id": id}
        self._database.delete(query=query, params=params)

    def delete_by_category(self, category_id: Union[str, int]) -> int:
        """Deletes the entities by category_id

        Args:
            category_id (Union[str,int]): Category identifier.

        """
        self._df = None
        query = f"DELETE FROM {self._name} WHERE category_id = :category_id;"
        params = {"category_id": category_id}
        self._database.delete(query=query, params=params)

    def delete_all(self) -> int:
        """Deletes all entities from the repository."""
        self._df = None

        query = f"DELETE FROM {self._name};"
        params = {}

        self._database.delete(query=query, params=params)

    def get_duplicates(self, by: str = "id") -> pd.DataFrame:
        """Returns duplicate rows examing the column or columns in 'by'.

        Args:
            by (str,list): A variable or list of variables in the repository.
        """
        df = self.getall()
        counts = df[by].value_counts(sort=True, ascending=False, normalize=False).reset_index()
        counts

    def dedup(self) -> None:
        """Removes duplicates in the repository"""

        df = self.getall()
        rows = df.shape[0]
        nids = df["id"].nunique()
        if rows != nids:
            self._df = None
            msg = f"\nThere are {rows} rows and {nids} unique ids. Do you want to dedup? (y/n)"
            dedup = input(msg)
            if "y" in dedup.lower():
                df2 = df.drop_duplicates()
                rows2 = df2.shape[0]
                nids2 = df2["id"].nunique()
                if rows == rows2:
                    msg = "There are no duplicate rows; however, there may be duplicate ids. Check your data."
                    self._logger.info(msg)
                else:
                    msg = (
                        f"\nDedup will reduce rows to {rows2} and {nids2} unique ids. Commit? (y/n)"
                    )
                    go = input(msg)
                    if "y" in go.lower():
                        self.replace(data=df2)
                        deleted = rows - rows2
                        msg = f"Removed {deleted} duplicates from the {self._name} repository."
                        self._logger.info(msg)
                        self.save()

    def save(self) -> None:
        """Saves the repository to file located in the designated directory."""
        self._database.commit()


# ------------------------------------------------------------------------------------------------ #
#                                       UNIT OF WORK BASE CLASS                                    #
# ------------------------------------------------------------------------------------------------ #
class UoW(ABC):
    """Unit of Work Base class, defining some basic functionality based upon the IUoW interface.

    This class should not be instantiated directly, instead subclasses should be used which
    contain the collection of repositories.
    Args:
        database (Database): A Database instance from the dependency injector container.

    """

    def __init__(
        self,
        database: Database,
    ) -> None:
        self._database = database
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def database(self) -> Database:
        return self._database

    def connect(self) -> None:
        """Connects the database"""
        self._database.connect()

    def begin(self) -> None:
        """Begin a transaction"""
        self._database.begin()

    def save(self) -> None:
        """Saves changes to the underlying sqlite context"""
        self._database.commit()

    def rollback(self) -> None:
        """Returns state of sqlite to the point of the last commit."""
        self._database.rollback()

    def close(self) -> None:
        """Closes the sqlite connection."""
        self._database.close()
