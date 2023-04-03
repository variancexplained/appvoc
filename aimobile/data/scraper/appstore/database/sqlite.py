#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/scraper/appstore/database/sqlite.py                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday March 30th 2023 03:03:56 pm                                                #
# Modified   : Sunday April 2nd 2023 01:23:39 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
import os
import logging

import pandas as pd
import sqlite3
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

from aimobile.data.scraper.appstore.database.base import Database


# ------------------------------------------------------------------------------------------------ #
class SQLiteDatabase(Database):
    """Encapsulates an SQLite database using an SQLAlchemy database engine.

    Args:
        filepath (str): The database relative filepath. Must be of form 'sqlite:///<filepath>'
    """

    def __init__(self, filepath: str) -> None:
        self._filepath = filepath
        self._engine = None
        self._connection = None
        self._transaction = None

        os.makedirs(self._filepath, exist_ok=True)
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    @property
    def filepath(self) -> str:
        """Returns the path to the database file."""
        return self._filepath

    def __enter__(self) -> SQLiteDatabase:
        """Enters a transaction block allowing multiple database operations to be performed as a unit."""
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # pragma: no cover
        """Special method takes care of properly releasing the object's resources to the operating system."""
        if exc_type is not None:
            try:
                self.rollback()
            except SQLAlchemyError as e:
                msg = f"Exception occurred.\nException type: {type[SQLAlchemyError]}\n{e}"
                self._logger.error(msg)
                raise
            msg = f"Exception occurred.\nException type: {exc_type}\n{exc_value}\n{traceback}"
            self._logger.error(msg)
            raise
        else:
            self.commit()
        self.close()

    def connect(self, autocommit: bool = False):
        """Connect to an underlying database.

        Args:
            autocommit (bool): Sets autocommit mode. Default is False.
        """
        try:
            self._engine = sqlalchemy.create_engine(self._filepath, echo=True, pool_pre_ping=True)
            self._connection = self._engine.connect()
            if autocommit is True:
                self._connection.execution_options(isolation_level="AUTOCOMMIT")
            else:
                self._connection.execution_options(isolation_level="READ UNCOMMITTED")
        except sqlite3.DatabaseError as e:  # pragma: no cover
            msg = f"Database connection failed.\nException type: {type[e]}\n{e}"
            self._logger.error(msg)
            raise e

    def begin(self):
        """Begins a transaction block."""
        try:
            self._transaction = self._connection.begin()
        except AttributeError:
            self.connect()
            self._transaction = self._connection.begin()

    def in_transaction(self) -> bool:
        """Queries the SQLite autocommit mode and returns True if the connection is in transaction."""
        try:
            return self._connection.in_transaction()
        except sqlite3.ProgrammingError:  # pragma: no cover
            # ProgrammingError raised if connection is closed.
            return False

    def commit(self) -> None:
        """Saves pending database operations to the database."""
        try:
            self._connection.commit()
        except sqlite3.DatabaseError as e:  # pragma: no cover
            msg = f"Exception occurred during connection commit.\n{e}"
            self._logger.error(msg)
            raise e
        except SQLAlchemyError as e:  # pragma: no cover
            msg = f"Exception occurred during connection commit.\n{e}"
            self._logger.error(msg)
            raise e

    def rollback(self) -> None:
        """Restores the database to the state of the last commit."""
        try:
            self._connection.rollback()
        except sqlite3.DatabaseError as e:  # pragma: no cover
            msg = f"Exception occurred during connection rollback.\n{e}"
            self._logger.error(msg)
            raise e
        except SQLAlchemyError as e:  # pragma: no cover
            msg = f"Exception occurred during connection rollback.\n{e}"
            self._logger.error(msg)
            raise e

    def close(self) -> None:
        """Closes the database connection."""
        try:
            self._connection.close()
        except sqlite3.DatabaseError as e:  # pragma: no cover
            msg = f"Database connection close failed.\nException type: {type[e]}\n{e}"
            self._logger.error(msg)
            raise e
        except SQLAlchemyError as e:  # pragma: no cover
            msg = f"Database connection close failed.\nException type: {type[e]}\n{e}"
            self._logger.error(msg)
            raise e

    def dispose(self) -> None:
        """Disposes the connection and releases resources."""
        try:
            self._engine.dispose()
        except sqlite3.DatabaseError as e:  # pragma: no cover
            msg = f"Database connection close failed.\nException type: {type[e]}\n{e}"
            self._logger.error(msg)
            raise e
        except SQLAlchemyError as e:  # pragma: no cover
            msg = f"Database connection close failed.\nException type: {type[e]}\n{e}"
            self._logger.error(msg)
            raise e

    def insert(self, data: pd.DataFrame, tablename: str) -> int:
        """Inserts data in pandas DataFrame format into the designated table.

        Note: This method uses pandas to_sql method. If not in transaction, inserts are
        autocommitted and rollback has no effect. Transaction behavior is extant
        after a begin() or through the use of the context manager.

        Args:
            data (pd.DataFrame): DataFrame containing the data to add to the designated table.
            tablename (str): The name of the table in the database. If the table does not
                exist, it will be created.

        Returns: Number of rows inserted.
        """
        try:
            return data.to_sql(tablename, con=self._connection, if_exists="append", index=False)
        except SQLAlchemyError as e:  # pragma: no cover
            msg = f"Exception occurred during database insert.\nException type:{type[SQLAlchemyError]}\n{e}"
            self._logger.error(msg)
            raise e
        except AttributeError as e:  # pragma: no cover
            msg = f"Exception occurred during database insert.\nException type:{type[AttributeError]}\nNo database connection.\n{e}"
            self._logger.error(msg)
            raise sqlite3.ProgrammingError()

    def update(self, query: str, params: tuple = None) -> int:
        """Updates row(s) matching the query.

        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        Returns (int): Number of rows updated.
        """
        result = self.execute(query=query, params=params)
        return result.rowcount

    def delete(self, query: str, params: tuple = None) -> int:
        """Deletes row(s) matching the query.

        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        Returns (int): Number of rows deleted.
        """
        result = self.execute(query=query, params=params)
        return result.rowcount

    def query(self, query: str, params: tuple = ()) -> pd.DataFrame:
        """Fetches the next row of a query result set, returning a single sequence, or None if no more data
        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        Returns: Pandas DataFrame

        """
        return pd.read_sql(sql=query, con=self._connection, params=params)

    def exists(self, query: str, params: tuple = None) -> bool:
        """Returns True if a row matching the query and parameters exists. Returns False otherwise.
        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        """
        result = self.execute(query=query, params=params)
        result = result.fetchall()
        return result != 0

    def execute(self, query: str, params: tuple = ()) -> list:
        """Execute method reserved primarily for updates, and deletes, as opposed to queries returning data.

        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        Returns (int): Number of rows updated or deleted.

        """
        return self._connection.execute(statement=sqlalchemy.text(query), parameters=params)
