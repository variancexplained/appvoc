#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/scraper/appstore/dal/appdata.py                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 06:01:22 am                                                  #
# Modified   : Sunday April 2nd 2023 07:54:01 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

import pandas as pd

from aimobile.data.scraper.appstore.dal.base import Repo
from aimobile.data.scraper.appstore.database.sqlite import SQLiteDatabase


# ------------------------------------------------------------------------------------------------ #
class AppStoreDataRepo(Repo):
    """Repository for app data from the Apple App Store

    Args:
        database (SQLiteDatabase): Appstore Database
    """

    def __init__(self, database: SQLiteDatabase) -> None:
        self._database = database
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def get(self, category: str) -> pd.DataFrame:
        """Retrieves AppData by category

        Args:
            category_name (str): A category_name from AppStoreCategories
        """
        query = "SELECT * FROM appdata WHERE appdata.category = :category;"
        params = {"category": category}
        return self._database.query(query=query, params=params)

    def add(self, data: pd.DataFrame) -> None:
        """Adds a DataFrame to the Database

        Args:
            data (pd.DataFrame): The data
        """
        self._database.insert(data=data, tablename="appdata")

    def update(self, data: pd.DataFrame) -> None:
        """Updates the table with the existing data.

        Args:
            data (pd.DataFrame): The data to replace existing data

        """
        raise NotImplementedError("App Data are immutable. Update is not implemented.")
