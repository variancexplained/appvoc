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
# Modified   : Monday April 10th 2023 11:07:48 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

import pandas as pd

from aimobile.scraper.appstore.repo.base import Repo
from aimobile.scraper.appstore.database.sqlite import SQLiteDatabase


# ------------------------------------------------------------------------------------------------ #
class AppStoreReviewRepo(Repo):
    """Repository of reviews from the Apple App Store

    Args:
        database (SQLiteDatabase): Appstore Database
    """

    def __init__(self, database: SQLiteDatabase) -> None:
        self._database = database
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def get(self, app_id: int) -> pd.DataFrame:
        """Retrieves reviews by app_id

        Args:
            category_name (str): A category_name from AppStoreCategories
        """
        query = "SELECT * FROM review WHERE review.app_id = :app_id;"
        params = {"app_id": app_id}
        return self._database.query(query=query, params=params)

    def get_by_category(self, category_id: int) -> pd.DataFrame:
        """Retrieves reviews by category_id

        Args:
            category_id (int): A category_id from AppStoreCategories
        """
        query = "SELECT * FROM review WHERE review.category_id = :category_id;"
        params = {"category_id": category_id}
        return self._database.query(query=query, params=params)

    def getall(self) -> pd.DataFrame:
        """Returns a DataFrame of all reviews in the repository"""
        query = "SELECT * FROM review;"
        df = self._database.query(query=query)
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

    def remove(self, id: int) -> None:
        """Removes review by id.

        Args:
            data (pd.DataFrame): The data to replace existing data

        """
        raise NotImplementedError("Review data are immutable. Remove is not implemented.")
