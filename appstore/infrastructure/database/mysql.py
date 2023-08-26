#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/infrastructure/database/mysql.py                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 10th 2023 09:50:40 pm                                                  #
# Modified   : Friday August 25th 2023 12:53:49 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""MySQL Database Module"""
from __future__ import annotations
import os

from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy
import subprocess
from time import sleep

from appstore.infrastructure.database.base import Database

# ------------------------------------------------------------------------------------------------ #
load_dotenv()


# ------------------------------------------------------------------------------------------------ #
class MySQLDatabase(Database):
    """MySQL Database Class
    Args:
        name (str): Name of database
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name
        self._connection_string = self._get_connection_string()
        self.connect()

    def connect(self, autocommit: bool = False) -> None:
        attempts = 0
        max_attempts = 3
        database_started = False
        while attempts < max_attempts:
            attempts += 1
            try:
                self._engine = sqlalchemy.create_engine(self._connection_string)
                self._connection = self._engine.connect()
                if autocommit is True:
                    self._connection.execution_options(isolation_level="AUTOCOMMIT")
                else:
                    self._connection.execution_options(isolation_level="READ UNCOMMITTED")
                self._is_connected = True
                database_started = True

            except SQLAlchemyError as e:  # pragma: no cover
                self._is_connected = False
                if not database_started:
                    msg = "Database is not started. Starting database..."
                    self._logger.info(msg)
                    self._start_db()
                    database_started = True
                    sleep(3)
                else:
                    msg = f"Database connection failed.\nException type: {type[e]}\n{e}"
                    self._logger.exception(msg)
                    raise
            else:
                return self

    def backup(self, filepath: str) -> None:
        """Performs a backup of the database to file

        Args:
            filepath (str): The backup file on the local file system.
        """
        script = os.getenv("MYSQL_BACKUP_SCRIPT")
        command = [script, "-d", self._name, "-f", filepath]
        subprocess.check_call(command, shell=True)

    def restore(self, filepath: str) -> None:
        """Restores the database from a backup file.

        Args:
            filepath (str): The backup file on the local file system.
        """
        script = os.getenv("MYSQL_RESTORE_SCRIPT")
        command = [script, "-d", self._name, "-f", filepath]
        subprocess.check_call(command, shell=True)

    def _get_connection_string(self) -> str:
        """Returns the connection string for the named database."""

        u = os.getenv("MYSQL_USERNAME")
        p = os.getenv("MYSQL_PWD")
        mode = os.getenv("MODE")
        self._name = f"{self._name}_test" if mode == "test" else self._name

        return f"mysql+pymysql://{u}:{p}@localhost/{self._name}"

    def _start_db(self) -> None:
        filepath = os.getenv("MYSSQL_STARTUP_SCRIPT")
        subprocess.run([filepath], shell=True)
