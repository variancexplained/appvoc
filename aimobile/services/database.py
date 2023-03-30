#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/services/database.py                                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday March 30th 2023 03:03:56 pm                                                #
# Modified   : Thursday March 30th 2023 05:19:21 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod
from typing import Any, Union
import logging

import pandas as pd
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError


# ------------------------------------------------------------------------------------------------ #
class Database(ABC):
    """Abstract base class for databases."""

    @abstractmethod
    def add(self, data: Any, tablename: str) -> None:
        """Adds data to the database

        Args:
            data (Any): Data to be added to the database
            tablename (str): Name of the table

        """

    @abstractmethod
    def get(self, query: str, params: tuple) -> Union[pd.DataFrame, list]:
        """Returns the results of he query from the database

        Args:
            query (str): An SQL Query
            params (tuple): Parameters for the SQL command
        """

    @abstractmethod
    def update(self, query: str, params: tuple) -> None:
        """Updates a row in the database

        Args:
            query (str): An SQL Query
            params (tuple): Parameters for the SQL command
        """

    @abstractmethod
    def remove(self, query: str, params: tuple) -> None:
        """Removes data from the database

        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        """

    @abstractmethod
    def exists(self, query: str, params: tuple) -> bool:
        """Checks existence of a row in the database

        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        """

    @abstractmethod
    def count(self, query: str, params: tuple) -> int:
        """Counts the rows matching the query

        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        """


# ------------------------------------------------------------------------------------------------ #
class SqliteDatabase(Database):
    """SQLite database

    Args:
        filepath (str): The database relative filepath. Must be of form 'sqlite:///<filepath>'
    """

    def __init__(self, filepath: str) -> None:
        self._filepath = filepath
        self._engine = sqlalchemy.create_engine(filepath)
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def add(self, data: pd.DataFrame, tablename: str) -> None:
        """Adds data to the database

        Args:
            data (Any): Pandas DataFrame

        """
        data.to_sql(tablename, con=self._engine, if_exists="append", index=False)

    def get(self, query: str, params: tuple) -> pd.DataFrame:
        """Returns the results of he query from the database

        Args:
            query (str): An SQL Query
            params (tuple): Parameters for the SQL command
        """
        return pd.read_sql(sql=query, con=self._engine, params=params)

    def update(self, query: str, params: tuple) -> None:
        """Updates a row in the database

        Args:
            query (str): An SQL Query
            params (tuple): Parameters for the SQL command
        """
        try:
            result = self._engine.execute(query, params)
        except SQLAlchemyError as e:
            msg = f"Exception occurred executing:\n\tQuery: {query}\n\tParams: {params}\n{e}"
            self._logger.error(msg)
            raise e
        else:
            msg = f"Query: {query}\nParams: {params}\nRecords updated: {result.rowcount}"
            self._logger.debug(msg)

    def remove(self, query: str, params: tuple) -> None:
        """Removes data from the database

        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        """
        try:
            result = self._engine.execute(query, params)
        except SQLAlchemyError as e:
            msg = f"Exception occurred executing:\n\tQuery: {query}\n\tParams: {params}\n{e}"
            self._logger.error(msg)
            raise e
        else:
            msg = f"Query: {query}\nParams: {params}\nRecords deleted: {result.rowcount}"
            self._logger.debug(msg)

    def exists(self, query: str, params: tuple) -> bool:
        """Checks existence of a row in the database

        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        """
        try:
            return self._engine.execute(query, params)
        except SQLAlchemyError as e:
            msg = f"Exception occurred executing:\n\tQuery: {query}\n\tParams: {params}\n{e}"
            self._logger.error(msg)
            raise e

    def count(self, query: str, params: tuple) -> int:
        """Counts the rows matching the query

        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        """
        df = self.get(query=query, params=params)
        return df.shape[0]
