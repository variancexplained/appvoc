#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/repo/rating.py                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 06:01:22 am                                                  #
# Modified   : Sunday April 16th 2023 02:32:25 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
import logging
import os
from itertools import count
from typing import Union

import pandas as pd

from aimobile.scraper.base import Repo
from aimobile.scraper.appstore.entity.rating import AppStoreRatings
from aimobile.scraper.appstore.database.base import Database
from aimobile import exceptions
from aimobile.utils.io import IOService


# ------------------------------------------------------------------------------------------------ #
class AppStoreRatingsRepo(Repo):
    """Repository for app ratings from the Apple App Store

    Args:
        database (SQLiteDatabase): Appstore Database
    """

    __file_seq = count(1)

    def __init__(self, database: Database) -> None:
        self._database = database
        self._file_seq = next(AppStoreRatingsRepo.__file_seq)
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def get(self, id: int) -> AppStoreRatings:
        """Retrieves App Ratings for the with the designated id.

        Args:
            id (int): An app id
        """
        query = "SELECT * FROM ratings WHERE id = :id;"
        params = {"id": id}
        df = self._database.query(query=query, params=params)
        if df.shape[0] == 0:
            raise exceptions.ObjectNotFound(id=id)
        else:
            return AppStoreRatings.from_df(df.loc[0])

    def getall(self) -> pd.DataFrame:
        """Retrieves all ratings"""
        query = "SELECT * FROM ratings;"
        df = self._database.query(query=query)
        if df.shape[0] == 0:
            raise exceptions.ObjectNotFound()
        else:
            return df

    def add(self, data: pd.DataFrame) -> None:
        """Adds a DataFrame to the Database

        Args:
            data (pd.DataFrame): The data
        """
        self._database.insert(data=data, tablename="ratings")

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
        query = "DELETE FROM ratings WHERE ratings.category_id = :category_id;"
        params = {"category_id": category_id}
        rowcount = self._database.delete(query=query, params=params)
        if rowcount == 0:
            raise exceptions.ObjectNotFound()

    def drop(self) -> None:
        """Drops the ratings table."""
        query = "DROP TABLE IF EXISTS ratings;"
        self._database.execute(query=query)

    def dedup(self) -> None:
        df = self.getall()
        df.drop_duplicates(keep="first", inplace=True)
        self._database.replace(data=df, tablename="ratings")

    def save(self, term: Union[str, int], directory: str) -> None:
        """Saves the database to file."""
        fileseq = str(self._file_seq).zfill(3)
        os.makedirs(directory, exist_ok=True)
        filename = "ratings_" + fileseq + "_" + str(term) + ".pkl"
        filepath = os.path.join(directory, filename)
        df = self.getall()
        IOService.write(filepath=filepath, data=df)
