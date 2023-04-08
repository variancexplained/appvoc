#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/service/scraper/appstore/repo/appdata.py                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 06:01:22 am                                                  #
# Modified   : Saturday April 8th 2023 10:46:35 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

import pandas as pd

from aimobile.service.scraper.base import Repo
from aimobile.service.scraper.appstore.entity.appdata import AppStoreAppData
from aimobile.service.scraper.appstore.database.base import Database
from aimobile import exceptions


# ------------------------------------------------------------------------------------------------ #
class AppStoreDataRepo(Repo):
    """Repository for app data from the Apple App Store

    Args:
        database (SQLiteDatabase): Appstore Database
    """

    def __init__(self, database: Database) -> None:
        self._database = database
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def get(self, id: int) -> AppStoreAppData:
        """Retrieves AppData by id

        Args:
            id (int): An app id
        """
        query = "SELECT * FROM appdata WHERE appdata.id = :id;"
        params = {"id": id}
        df = self._database.query(query=query, params=params)
        if df.shape[0] == 0:
            raise exceptions.AppNotFound(id=id)
        else:
            return AppStoreAppData.from_df(df.loc[0])

    def getall(self) -> pd.DataFrame:
        """Retrieves all appdata"""
        query = "SELECT * FROM appdata;"
        df = self._database.query(query=query)
        if df.shape[0] == 0:
            raise exceptions.AppsNotFound()
        else:
            return df

    def get_category(self, category_id: int) -> pd.DataFrame:
        """Retrieves AppData by category id

        Args:
            category_id (int): A category_id from AppStoreCategories
        """
        query = "SELECT * FROM appdata WHERE appdata.category_id = :category_id;"
        params = {"category_id": category_id}
        df = self._database.query(query=query, params=params)
        if df.shape[0] == 0:
            raise exceptions.AppsNotFound()
        else:
            return df

    def add(self, data: pd.DataFrame) -> None:
        """Adds a DataFrame to the Database

        Args:
            data (pd.DataFrame): The data
        """
        self._database.insert(data=data, tablename="appdata")

    def update(self, data: pd.DataFrame) -> None:  # pragma: no cover
        """Updates the table with the existing data.

        Args:
            data (pd.DataFrame): The data to replace existing data

        """
        raise NotImplementedError("App Data are immutable. Update is not implemented.")

    def remove(self, category_id: int) -> None:
        """Removes apps in the designated category

        Args:
            category_id (int): A four digit identifier for the category from AppStoreCategories

        """
        query = "DELETE FROM appdata WHERE appdata.category_id = :category_id;"
        params = {"category_id": category_id}
        rowcount = self._database.delete(query=query, params=params)
        if rowcount == 0:
            raise exceptions.AppsNotFound()
