#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/scraper/appstore/database/base.py                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 11:34:11 am                                                  #
# Modified   : Sunday April 2nd 2023 11:08:59 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module provides basic database interface"""
from __future__ import annotations
from abc import ABC, abstractmethod

import pandas as pd


# ------------------------------------------------------------------------------------------------ #
class Database(ABC):
    """Abstract base class for databases."""

    @property
    @abstractmethod
    def filepath(self) -> str:
        """Returns the path to the database file."""

    @abstractmethod
    def __enter__(self) -> Database:
        """Enters a transaction block allowing multiple database operations to be performed as a unit."""

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Special method takes care of properly releasing the object's resources to the operating system."""

    @abstractmethod
    def connect(self) -> None:
        """Connect to an underlying database."""

    @abstractmethod
    def begin(self) -> None:
        """Starts a transaction block."""

    @abstractmethod
    def in_transaction(self) -> bool:
        """Queries the SQLite autocommit mode and returns True if the connection is in transaction."""

    @abstractmethod
    def commit(self) -> None:
        """Saves pending database operations to the database."""

    @abstractmethod
    def rollback(self) -> None:
        """Restores the database to the state of the last commit."""

    @abstractmethod
    def close(self) -> None:
        """Closes the database connection."""

    @abstractmethod
    def dispose(self) -> None:
        """Disposes the connection and releases resources."""

    @abstractmethod
    def insert(self, data: pd.DataFrame, tablename: str) -> int:
        """Inserts data in pandas DataFrame format into the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing the data to add to the designated table.
            tablename (str): The name of the table in the database. If the table does not
                exist, it will be created.
        """

    @abstractmethod
    def update(self, query: str, params: tuple = None) -> int:
        """Updates row(s) matching the query.

        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        Returns (int): Number of rows updated.
        """

    @abstractmethod
    def delete(self, query: str, params: tuple = None) -> int:
        """Deletes row(s) matching the query.

        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        Returns (int): Number of rows deleted.
        """

    @abstractmethod
    def query(self, query: str, params: tuple = None) -> pd.DataFrame:
        """Queries the database and returns rows matching the query in Pandas DataFrame format"""

    @abstractmethod
    def exists(self, query: str, params: tuple = None) -> bool:
        """Returns True if a row matching the query and parameters exists. Returns False otherwise.
        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        """

    @abstractmethod
    def execute(self, query: str, params: tuple = None) -> int:
        """Execute commands on the underlying database.

        Args:
            query (str): The SQL command
            params (tuple): Parameters for the SQL command

        Returns (SQLAlchemy.CursorResult)
        """
