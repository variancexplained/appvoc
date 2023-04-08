#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Opportunity Discovery in Mobile Applications                             #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/scraper/appstore/dal/appdata.py                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 06:01:22 am                                                  #
# Modified   : Thursday April 6th 2023 02:07:46 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

import pandas as pd

from aimobile.data.scraper.base import Repo
from aimobile.data.scraper.appstore.database.base import Database


# ------------------------------------------------------------------------------------------------ #
class AppStoreDataRepo(Repo):
    """Repository for app data from the Apple App Store

    Args:
        database (SQLiteDatabase): Appstore Database
    """

    def __init__(self, database: Database) -> None:
        self._database = database
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def load(self, data: list) -> None:
        """Loads a list of AppDetail objects into the database.

        Args:
            data (list): List of AppStoreAppData objects
        """
        # Convert the list of AppStoreAppData objects into  a list of dictionaries.
        lod = [app.as_dict() for app in data]
        df = pd.DataFrame(data=lod)
        self._database.insert(data=df, tablename="appdata")

    def get(self, category_id: str) -> pd.DataFrame:
        """Retrieves AppData by category id

        Args:
            category_id (int): A category_id from AppStoreCategories
        """
        query = "SELECT * FROM appdata WHERE appdata.category_id = :category_id;"
        params = {"category_id": category_id}
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

    def remove(
        self,
        id: int = None,
        category_id: int = None,
        collection: str = None,
    ) -> None:
        """Removies data from the database

        All parameters are optional; however, if no values are passed, nothing
        is removed.

        Args:
            id (int): Id for the row to be deleted.
            category_id (int): A four digit identifier for the category from AppStoreCategories
            collection (str): A collection from which rows are to be deleted. Must be
                one of AppStoreCollections

        """
        if category_id is not None and collection is not None:
            query = "DELETE FROM appdata WHERE appdata.category_id = :cid, AND appdata.collection = :col;"
            params = {"cid": category_id, "col": collection}
        elif category_id is not None:
            query = "DELETE FROM appdata WHERE appdata.category_id = :cid;"
            params = {"cid": category_id}
        elif collection is not None:
            query = "DELETE FROM appdata WHERE appdata.collection = :col;"
            params = {"col": collection}
        elif id is not None:
            query = "DELETE FROM appdata WHERE appdata.id = :id;"
            params = {"id": id}
        self._database.execute(query=query, params=params)

    def save(self) -> None:
        """Commits the changes to the underlying database."""
        self._database.commit()
