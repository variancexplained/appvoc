#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/database/sqlite.py                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday March 30th 2023 03:03:56 pm                                                #
# Modified   : Sunday April 16th 2023 03:42:07 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
import os

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

from aimobile.scraper.appstore.database.base import Database


# ------------------------------------------------------------------------------------------------ #
class SQLiteDatabase(Database):
    """Encapsulates an SQLite database using an SQLAlchemy database engine.

    Args:
        filepath (str): The database relative filepath. Must be of form 'sqlite:///<filepath>'
    """

    def __init__(self, filepath: str) -> None:
        super().__init__()
        self._filepath = filepath
        os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
        self._filepath = (
            "sqlite:///" + self._filepath
        )  # Added as per https://docs.sqlalchemy.org/en/14/core/engines.html#sqlite

    @property
    def filepath(self) -> str:
        """Returns the path to the database file."""
        return self._filepath

    def connect(self, autocommit: bool = False):
        """Connect to an underlying database.

        Args:
            autocommit (bool): Sets autocommit mode. Default is False.
        """
        try:
            self._engine = sqlalchemy.create_engine(self._filepath, echo=False, pool_pre_ping=True)
            self._connection = self._engine.connect()
            if autocommit is True:
                self._connection.execution_options(isolation_level="AUTOCOMMIT")
            else:
                self._connection.execution_options(isolation_level="READ UNCOMMITTED")
            self._is_connected = True
            return self
        except SQLAlchemyError as e:  # pragma: no cover
            self._is_connected = False
            msg = f"Database connection failed.\nException type: {type[e]}\n{e}"
            self._logger.error(msg)
            raise e
