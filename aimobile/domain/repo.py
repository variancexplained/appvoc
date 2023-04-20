#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/abc/repo.py                                                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 19th 2023 11:17:34 am                                               #
# Modified   : Wednesday April 19th 2023 08:04:21 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod
from typing import Union

import pandas as pd


# ------------------------------------------------------------------------------------------------ #
class RepoABC(ABC):
    """Provides a generic repository interface.

    Args:
        database(Database): Database containing data to access.
    """

    @abstractmethod
    def add(self, data: pd.DataFrame, tablename: str) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
            tablename (str): Table to which the data must be added.
        """

    @abstractmethod
    def get(self, tablename: str, id: Union[str, int]) -> pd.DataFrame:
        """Returns all data in the designated table in DataFrame format.

        Args:
            id (Union[str,int]): App id.
            tablename (str): The table from which the data is to be obtained.
        """

    @abstractmethod
    def get_by_category(self, category_id: Union[str, int], tablename: str) -> pd.DataFrame:
        """Obtains data from the given table by category id

        Args:
            category_id (Union[str,int]): The mobile app category.
            tablename (str): An existing table in the database.
        """

    @abstractmethod
    def exists(self, id: Union[str, int], tablename: str = "appdata") -> bool:
        """Assesses the existence of an app in the database.

        Args:
            id (Union[str,int]): The app id.
            tablename (str): The 'appdata' table.
        """

    @abstractmethod
    def count(self, tablename: str, id: Union[str, int] = None) -> int:
        """Counts the rows matching the criteria. Counts all rows if id is None.

        Args:
            tablename (str): The name of the table
            id (Union[str,int]): The app id

        Returns number of rows matching criteria
        """

    @abstractmethod
    def delete(self, tablename: str, id: Union[str, int] = None) -> int:
        """Deletes the row designated by the tablename an id. Deletes all rows if id is None

        Args:
            tablename (str): The name of the table
            id (Union[str,int]): The app id

        Returns number of rows deleted.

        """

    @abstractmethod
    def save(self) -> None:
        """Saves changes to the underlying database"""
