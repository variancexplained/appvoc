#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/framework/database/mysql.py                                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 10th 2023 09:50:40 pm                                                  #
# Modified   : Tuesday April 18th 2023 10:57:42 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""MySQL Database Module"""
from __future__ import annotations
import os
from dotenv import load_dotenv
import subprocess

from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy

from aimobile.framework.database.base import Database

# ------------------------------------------------------------------------------------------------ #
load_dotenv()


# ------------------------------------------------------------------------------------------------ #
class MySQLDatabase(Database):
    """MySQL Database Class
    Args:
        name (str): Name of database in ['appstore','googleplay']
        mode (str): Mode in ['prod', 'dev', 'test']. Defaults to mode set in environment variable
    """

    __dbnames = ["appstore", "googleplay"]

    def __init__(self, name: str) -> None:
        super().__init__()
        if name not in MySQLDatabase.__dbnames:
            self._logger.error(
                f"There is no database named {name}. Valid names are {MySQLDatabase.__dbnames}"
            )
        self._name = name
        self._connection_string = self._get_connection_string()

    @property
    def name(self) -> str:
        """Returns the name of the database"""
        return self._name

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
        u = os.getenv("MYSQL_USERNAME")
        p = os.getenv("MYSQL_PWD")
        dbname = self._name + "_" + mode
        return f"mysql+pymysql://{u}:{p}@localhost/{dbname}"


# ------------------------------------------------------------------------------------------------ #
class MySQLServer:
    """Encapsulates basic MySQL server commands"""

    __start_script = "scripts/database/management/start.sh"
    __restart_script = "scripts/database/management/restart.sh"
    __stop_script = "scripts/database/management/stop.sh"

    def start(self) -> None:
        subprocess.run(MySQLServer.__start_script)

    def restart(self) -> None:
        subprocess.run(MySQLServer.__restart_script)

    def stop(self) -> None:
        subprocess.run(MySQLServer.__stop_script)
