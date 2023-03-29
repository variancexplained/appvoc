#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/base.py                                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 01:57:39 pm                                                  #
# Modified   : Monday March 27th 2023 08:46:25 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod

import pandas as pd

from itunes_app_scraper.util import AppStoreCategories

# ------------------------------------------------------------------------------------------------ #
APPLE_CATEGORIES = {
    "BOOKS": AppStoreCategories.BOOKS,
    "BUSINESS": AppStoreCategories.BUSINESS,
    "EDUCATION": AppStoreCategories.EDUCATION,
    "ENTERTAINMENT": AppStoreCategories.ENTERTAINMENT,
    "HEALTH_AND_FITNESS": AppStoreCategories.HEALTH_AND_FITNESS,
    "LIFESTYLE": AppStoreCategories.LIFESTYLE,
    "FOOD_AND_DRINK": AppStoreCategories.FOOD_AND_DRINK,
    "SHOPPING": AppStoreCategories.SHOPPING,
    "MEDICAL": AppStoreCategories.MEDICAL,
    "TRAVEL": AppStoreCategories.TRAVEL,
    "PRODUCTIVITY": AppStoreCategories.PRODUCTIVITY,
    "SOCIAL_NETWORKING": AppStoreCategories.SOCIAL_NETWORKING,
    "SPORTS": AppStoreCategories.SPORTS,
    "MUSIC": AppStoreCategories.MUSIC,
    "PHOTO_AND_VIDEO": AppStoreCategories.PHOTO_AND_VIDEO,
    "REFERENCE": AppStoreCategories.REFERENCE,
    "NAVIGATION": AppStoreCategories.NAVIGATION,
    "UTILS": AppStoreCategories.UTILITIES,
}


# ------------------------------------------------------------------------------------------------ #
class AppCentre(ABC):
    """Abstract base class for Apple and Google data."""

    @abstractmethod
    def get_category_data(self, category: str) -> pd.DataFrame:
        """Returns a DataFrame with app data for a category.

        Args:
            category (str): The app category
        """

    @abstractmethod
    def get_category_reviews(self, category: str) -> pd.DataFrame:
        """Return the reviews for a category in DataFrame format.

        Args:
            category (str): The app category
        """

    @abstractmethod
    def get_app_data(self, app_id: int) -> dict:
        """Return the app data

        Args:
            app_id (int): The app id
        """

    @abstractmethod
    def get_app_review(self, app_id: int) -> dict:
        """Return the app review

        Args:
            app_id (int): The app id
        """


# ------------------------------------------------------------------------------------------------ #
class AppCentreBuilder(ABC):
    """Base class for the Apple and Google Play Data builders

    Args:
        directory (str): The home directory for the data.
    """

    @property
    @abstractmethod
    def appcentre(self) -> AppCentre:
        """Returns an AppCentre object encapsulating a catagory"""

    @abstractmethod
    def build_app_centre(self, directory: str) -> None:
        """Method that controls the construction of the AppCentre

        Args:
            directory (str): The home directory for the AppCentre.

        """

    @abstractmethod
    def _build_category(self, category: str, category_id: int) -> None:
        """Constructs data and reviews for a category

        Args:
            category (str): The app category.
        """

    @abstractmethod
    def _build_save_category_data(self, category: str, add_ids: list) -> pd.DataFrame:
        """Constructs data for a category and returns a Dataframe

        Args:
            category (str): The category
            add_ids (str): The app_ids in category.
        """

    @abstractmethod
    def _build_save_category_reviews(self, category: str, add_data: pd.DataFrame) -> None:
        """Constructs reviews for a category

        Args:
            category (str): The category
            add_ids (list): The app_ids in the category
        """

    @abstractmethod
    def _save(self, filename: str, data: pd.DataFrame) -> None:
        """Saves the category data to file

        Args:
            category (str): The app category.
            reviews (pd.DataFrame): The DataFrame containing the app reviews.
        """
