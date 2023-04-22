#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/domain/repo.py                                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 19th 2023 11:17:34 am                                               #
# Modified   : Saturday April 22nd 2023 03:14:32 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod
from typing import Union

import pandas as pd

from aimobile.infrastructure.dal.base import Database


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
        query = f"SELECT * FROM {self._name};"
        params = None
        return self._database.query(query=query, params=params)

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

        Returns number of rows deleted.
        """
        query = f"DELETE FROM {self._name} WHERE id = :id;"
        params = {"id": id}
        self._database.delete(query=query, params=params)

    def delete_all(self) -> int:
        """Deletes all entities from the repository."""

        query = f"DELETE FROM {self._name};"
        params = {}

        self._database.delete(query=query, params=params)

    def dedup(self) -> None:
        """Removes duplicates in the repository"""
        df = self.getall()
        before = len(df)

        df.drop_duplicates(keep="first", inplace=True)
        after = len(df)

        if before > after:
            self.delete_all()
            self.add(data=df)
            duplicates = before - after
            msg = f"Removed {duplicates} duplicates from the {self._name} repository."
            self._logger.info(msg)

    @abstractmethod
    def summarize(self) -> pd.DataFrame:
        """Summarize contents of Repository"""

    def save(self) -> None:
        """Saves the repository to file located in the designated directory."""
        self._database.commit()
