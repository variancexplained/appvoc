#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/base.py                                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday March 29th 2023 07:24:48 pm                                               #
# Modified   : Wednesday March 29th 2023 08:40:01 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod

import pandas as pd


# ------------------------------------------------------------------------------------------------ #
class AppData(ABC):
    """Abstract base class for app data"""

    @abstractmethod
    def scrape(self, category: str) -> None:
        """Scrapes data for the category and saves it as a pandas dataframe in the designated directory.

        The filename is of the format <category>_data.json.

        Args:
            category (str): Single word search term for the category of interest.

        """

    @abstractmethod
    def read(self, category: str) -> pd.DataFrame:
        """Returns the app data for the designated category

        Args:
            category (str): Single word search term for the category of interest.
        """

    @abstractmethod
    def write(self, data: pd.DataFrame, category: str) -> None:
        """Saves the app data to file.

        Args:
            data (pd.DataFrame): Dataframe containing the app data.
            category (str): The category of the data

        """

    @abstractmethod
    def summary(self) -> None:
        """Prints a summary of app scrapes."""


# ------------------------------------------------------------------------------------------------ #
class AppReviews(ABC):
    """Abstract base class for app reviews."""

    @abstractmethod
    def scrape(self, id: int) -> None:
        """Scrapes reviews for the app designated by the its id.

        Args:
            id (int): The id for the app of interest.

        """

    @abstractmethod
    def read(self, id: int) -> pd.DataFrame:
        """Returns the reviews for the app designated by its id.

        Args:
            id (int): The id for the app of interest.
        """

    @abstractmethod
    def write(self, data: pd.DataFrame, id: int) -> None:
        """Saves the app reviews for the designated app to file.

        Args:
            data (pd.DataFrame): Dataframe containing the app data.
            id (int): The id for the app of interest.

        """
