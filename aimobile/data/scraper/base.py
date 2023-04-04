#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/data/scraper/base.py                                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 3rd 2023 12:36:15 am                                                   #
# Modified   : Tuesday April 4th 2023 02:42:07 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Base class for the Scraper service."""
from __future__ import annotations
import sys
from abc import ABC, abstractmethod


# ------------------------------------------------------------------------------------------------ #
IMMUTABLE_TYPES: tuple = (str, int, float, bool, type(None))
SEQUENCE_TYPES: tuple = (list, tuple)


# ------------------------------------------------------------------------------------------------ #
#                                  ABSTRACT SCRAPER FACTORY                                        #
# ------------------------------------------------------------------------------------------------ #
class AbstractScraperFactory(ABC):
    """Defines a factory interface with methods that return abstract appdata and review scrapers"""

    @abstractmethod
    def create_appdata_scraper(self) -> AbstractAppDataScraper:
        """Returns a concrete AppDataScraper

        Args:
            project (AbtractScraperProject): Object defining the projecturation for the scraper.
        """

    @abstractmethod
    def create_review_scraper(self) -> AbstractReviewScraper:
        """Returns a concrete ReviewScraper

        Args:
            project (AbtractScraperProject): Object defining the projecturation for the scraper.
        """


# ------------------------------------------------------------------------------------------------ #
#                              ABSTRACT APPDATA SCRAPER                                            #
# ------------------------------------------------------------------------------------------------ #
class AbstractAppDataScraper(ABC):
    """Defines the interface for app data scrapers."""

    def search(
        self,
        term: str,
        lang: str = "en",
        country: str = "us",
        num: int = 200,
        pages: int = sys.maxsize,
        retries: int = 5,
        backoff_base: int = 2,
        sleep: tuple = (),
    ) -> list:
        """Retrieve app data for a search query

        Args:
            term (str): Search query
            lang (str): The language code to search. Default = 'en'
            country (str): The two-letter country code
            num (int): The number of items to return per page
            pages (int): The number of pages to return

        Return: List of dictionaries containing app details.
        """

    def category(
        self,
        category: str,
        lang: str = "en",
        country: str = "us",
        num: int = 200,
        pages: int = sys.maxsize,
    ) -> list:
        """Retrieves app details for the designated category

        Args:
            category  (str): Category of apps
            lang (str): The language code to search. Default = 'en'
            country (str): The two-letter country code
            num (int): The number of items to return per page
            pages (int): The number of pages to return

        Return: List of dictionaries containing app details.
        """


# ------------------------------------------------------------------------------------------------ #
#                              ABSTRACT REVIEW SCRAPER                                             #
# ------------------------------------------------------------------------------------------------ #
class AbstractReviewScraper(ABC):
    """Defines the interface for review scrapers."""
