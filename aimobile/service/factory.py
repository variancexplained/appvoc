#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /service/factory.py                                                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 3rd 2023 12:36:15 am                                                   #
# Modified   : Thursday April 20th 2023 07:03:38 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Base classes shared by both appstore and google scraping services."""
from __future__ import annotations
from abc import ABC, abstractmethod

from aimobile.service.scraper import AppScraper, ReviewScraper, RatingScraper


# ------------------------------------------------------------------------------------------------ #
#                                  ABSTRACT SCRAPER FACTORY                                        #
# ------------------------------------------------------------------------------------------------ #
class AbstractScraperFactory(ABC):
    """Defines a factory interface with methods that return abstract appdata and review scrapers"""

    @abstractmethod
    def create_appdata_scraper(self) -> AppScraper:
        """Returns a concrete AppDataScraper

        Args:
            project (AbtractScraperProject): Object defining the projecturation for the scraper.
        """

    @abstractmethod
    def create_rating_scraper(self) -> RatingScraper:
        """Returns a concrete AppDataScraper

        Args:
            project (AbtractScraperProject): Object defining the projecturation for the scraper.
        """

    @abstractmethod
    def create_review_scraper(self) -> ReviewScraper:
        """Returns a concrete ReviewScraper

        Args:
            project (AbtractScraperProject): Object defining the projecturation for the scraper.
        """
