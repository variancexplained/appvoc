#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/infrastructure/dal/sqlite.py                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday April 18th 2023 05:02:58 pm                                                 #
# Modified   : Thursday April 20th 2023 10:49:31 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy

from aimobile.infrastructure.dal.base import Database

# ------------------------------------------------------------------------------------------------ #
load_dotenv()


# ------------------------------------------------------------------------------------------------ #
class SQLiteDatabase(Database):
    """SQLite Database Class
    Args:
        name (str): Name of database in ['appstore','googleplay']
        mode (str): Mode in ['prod', 'dev', 'test']. Defaults to mode set in environment variable
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name
        self._connection_string = self._get_connection_string()
        self.connect()

    def connect(self, autocommit: bool = False) -> None:
        try:
            self._engine = sqlalchemy.create_engine(self._connection_string)
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

    def _get_connection_string(self) -> str:
        """Returns the connection string for the named database."""

        mode = os.getenv("MODE")
        filepath = f"aimobile/data/{self._name}/envs/{mode}/data/database.db"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        return f"sqlite:///{filepath}"
