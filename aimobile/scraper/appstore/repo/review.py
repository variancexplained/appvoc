#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/repo/review.py                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 06:23:39 am                                                  #
# Modified   : Sunday April 16th 2023 02:24:30 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging
import os
from itertools import count
from typing import Union

import pandas as pd

from aimobile.scraper.appstore.repo.base import Repo
from aimobile.scraper.appstore.database.mysql import MySQLDatabase
from aimobile.scraper.appstore.entity.review import AppStoreReview
from aimobile import exceptions
from aimobile.utils.io import IOService


# ------------------------------------------------------------------------------------------------ #
class AppStoreReviewRepo(Repo):
    """Repository of reviews from the Apple App Store

    Args:
        database (SQLiteDatabase): Appstore Database
    """

    __file_seq = count(1)

    def __init__(self, database: MySQLDatabase) -> None:
        self._database = database
        self._file_seq = next(AppStoreReviewRepo.__file_seq)
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def get(self, id: int) -> pd.DataFrame:
        """Retrieves review by id

        Args:
            id (int): A review identifier.
        """
        query = "SELECT * FROM review WHERE review.id = :id;"
        params = {"id": id}
        df = self._database.query(query=query, params=params)
        if df.shape[0] == 0:
            raise exceptions.ObjectNotFound(id=id)
        else:
            return AppStoreReview.from_df(df.loc[0])

    def get_by_category(self, category_id: int) -> pd.DataFrame:
        """Retrieves reviews by category_id

        Args:
            category_id (int): A category_id from AppStoreCategories
        """
        query = "SELECT * FROM review WHERE review.category_id = :category_id;"
        params = {"category_id": category_id}
        df = self._database.query(query=query, params=params)
        if df.shape[0] == 0:
            raise exceptions.ObjectNotFound()
        else:
            return df

    def getall(self) -> pd.DataFrame:
        """Returns a DataFrame of all reviews in the repository"""
        query = "SELECT * FROM review;"
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
        self._database.insert(data=data, tablename="review")

    def update(self, data: pd.DataFrame) -> None:
        """Updates the table with the existing data.

        Args:
            data (pd.DataFrame): The data to replace existing data

        """
        raise NotImplementedError("Request data are immutable. Update is not implemented.")

    def remove(self, app_id: int) -> None:
        """Removes review by app_id.

        Args:
            app_id (int): The app id

        """
        query = "DELETE FROM review WHERE review.app_id =:app_id;"
        params = {"app_id": app_id}
        self._database.execute(query=query, params=params)

    def drop(self) -> None:
        """Drops the review table."""
        query = "DROP TABLE IF EXISTS review;"
        self._database.execute(query=query)

    def dedup(self) -> None:
        df = self.getall()
        df.drop_duplicates(keep="first", inplace=True)
        self._database.replace(data=df, tablename="review")

    def save(self, term: Union[str, int], directory: str) -> None:
        """Saves the database to file."""
        fileseq = str(self._file_seq).zfill(3)
        os.makedirs(directory, exist_ok=True)
        filename = "reviews_" + fileseq + "_" + str(term) + ".csv"
        filepath = os.path.join(directory, filename)
        df = self.getall()
        IOService.write(filepath=filepath, data=df)
