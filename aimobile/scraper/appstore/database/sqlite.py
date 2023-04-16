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
# Modified   : Thursday April 13th 2023 04:38:45 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
import os

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
