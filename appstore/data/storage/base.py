#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/repo/base.py                                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 11:34:11 am                                                  #
# Modified   : Wednesday July 26th 2023 09:59:33 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module provides basic database interface"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union

import pandas as pd

from appstore.infrastructure.database.base import Database

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

    def reset(self) -> None:
        """Resets the repository by dropping the underlying table."""
        x = input(
            "This will delete the underlying table and commit the database. Type 'YES' to proceed."
        )
        if x == "YES":
            query = f"DROP TABLE IF EXISTS {self._name};"
            params = None
            self._database.execute(query=query, params=params)
            self.save()
            msg = f"Repository {self.__class__.__name__} reset."
            self._logger.info(msg)

    def sample(self, n: int = 5, frac: float = None, random_state: int = None) -> pd.DataFrame:
        """Returns a random sample from the underlying dataset.

        Args:
            n (int): Number of samples to return.
            frac (float): Proportion of the data to return. n is ignored
                if this variable is non-null.
            random_state (int): Seed for pseudo random generation.
        """
        df = self.getall()
        return df.sample(n=n, frac=frac).T

    def info(self) -> pd.DataFrame:
        """Wrapper for pandas info method"""
        df = self.getall()
        return df.info()

    def get(
        self, id: Union[str, int], dtypes: dict = None, parse_dates: dict = None
    ) -> pd.DataFrame:
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
            dtypes (dict): Dictionary mapping of column to data types
            parse_dates (dict): Dictionary of columns and keyword arguments for datetime parsing.
        """

        query = f"SELECT * FROM {self._name} WHERE id = :id;"
        params = {"id": id}
        return self._database.query(
            query=query, params=params, dtypes=dtypes, parse_dates=parse_dates
        )

    def get_by_category(
        self, category_id: Union[str, int], dtypes: dict = None, parse_dates: dict = None
    ) -> pd.DataFrame:
        """Obtains data from the given table by category id

        Args:
            category_id (Union[str,int]): The mobile app category.
            dtypes (dict): Dictionary mapping of column to data types
            parse_dates (dict): Dictionary of columns and keyword arguments for datetime parsing.
        """
        query = f"SELECT * FROM {self._name} WHERE category_id = :category_id;"
        params = {"category_id": category_id}
        return self._database.query(
            query=query, params=params, dtypes=dtypes, parse_dates=parse_dates
        )

    def getall(self, dtypes: dict = None, parse_dates: dict = None) -> pd.DataFrame:
        """Returns all data in the repository.

        Args:
            dtypes (dict): Dictionary mapping of column to data types
            parse_dates (dict): Dictionary of columns and keyword arguments for datetime parsing.
        """
        query = f"SELECT * FROM {self._name};"
        params = None
        return self._database.query(
            query=query, params=params, dtypes=dtypes, parse_dates=parse_dates
        )

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

        return self._database.query(query=query, params=params).shape[0]

    def delete(self, id: Union[str, int]) -> int:
        """Deletes the entity designated by the id.

        Args:
            id (Union[str,int]): Entity id

        """
        query = f"DELETE FROM {self._name} WHERE id = :id;"
        params = {"id": id}
        self._database.delete(query=query, params=params)

    def delete_by_category(self, category_id: Union[str, int]) -> int:
        """Deletes the entities by category_id

        Args:
            category_id (Union[str,int]): Category identifier.

        """
        query = f"DELETE FROM {self._name} WHERE category_id = :category_id;"
        params = {"category_id": category_id}
        self._database.delete(query=query, params=params)

    def delete_all(self) -> int:
        """Deletes all entities from the repository."""

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

    def dedup(self, keep: str = "last") -> None:
        """Removes duplicates in the repository"""

        df = self.getall()
        rows = df.shape[0]
        nids = df["id"].nunique()
        if rows != nids:
            msg = f"\nThere are {rows} rows and {nids} unique ids. Do you want to dedup? (y/n)"
            dedup = input(msg)
            if "y" in dedup.lower():
                df2 = df.drop_duplicates(keep=keep)
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
