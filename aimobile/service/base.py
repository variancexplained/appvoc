#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/service/base.py                                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday April 20th 2023 05:33:57 am                                                #
# Modified   : Saturday April 22nd 2023 10:15:47 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod


# ------------------------------------------------------------------------------------------------ #
class Controller(ABC):
    """Scraper controller responsible for scraping and persisting a target or series of URLs."""

    @abstractmethod
    def scrape(self, *args, **kwargs) -> None:
        """Scrapes data from the target url"""


# ------------------------------------------------------------------------------------------------ #
class AppScraper(ABC):
    """Defines the Scraper interface for app scraper objects returning app data in batch pages"""


# ------------------------------------------------------------------------------------------------ #
class ReviewScraper(ABC):
    """Defines the Scraper interface for review scrapers which return reviews, one-app at a time"""


# ------------------------------------------------------------------------------------------------ #
class RatingScraper(ABC):
    """Defines the Scraper interface for rating scrapers which return ratings, one-app at a time."""
