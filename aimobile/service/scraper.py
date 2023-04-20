#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /service/scraper.py                                                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday April 20th 2023 05:33:57 am                                                #
# Modified   : Thursday April 20th 2023 07:02:03 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod
from typing import Union

import pandas as pd


# ------------------------------------------------------------------------------------------------ #
class AppScraper(ABC):
    """Defines the Scraper interface for app scraper objects returning app data in batch pages"""

    @abstractmethod
    def search(self, term: str, *args, **kwargs) -> pd.DataFrame:
        """Searchese all apps matching the search term, parses and returns the result.

        Args:
            term (str): Search term

        Return: Page data are parsed and returned in DataFrame format.
        """


# ------------------------------------------------------------------------------------------------ #
class ReviewScraper(ABC):
    """Defines the Scraper interface for review scrapers which return reviews, one-app at a time"""

    @abstractmethod
    def reviews(self, id: Union[int, str], *args, **kwargs) -> pd.DataFrame:
        """Returns pages of reviews for the app designated by the id

        Args:
            id (Union[int,str]): App id

        Return: Page data are parsed and returned in DataFrame format.between progress resports to std.out.
        """


# ------------------------------------------------------------------------------------------------ #
class RatingScraper(ABC):
    """Defines the Scraper interface for rating scrapers which return ratings, one-app at a time."""

    @abstractmethod
    def ratings(self, id: Union[int, str], *args, **kwargs) -> pd.DataFrame:
        """Returns rating histogram data or an app.

        Args:
            id (Union[int,str]): App id

        Return: Page data are parsed and returned in DataFrame format.between progress resports to std.out.
        """
