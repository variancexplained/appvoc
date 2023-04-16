#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/database/mysql.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 10th 2023 09:50:40 pm                                                  #
# Modified   : Thursday April 13th 2023 04:39:23 pm                                                #
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

from aimobile.scraper.appstore.database.base import Database


# ------------------------------------------------------------------------------------------------ #
class MySQLDatabase(Database):
    """MySQL Database Class"""

    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name
        load_dotenv()
        self._connection_string = os.getenv("MYSQL")

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
