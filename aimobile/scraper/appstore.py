#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore.py                                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday March 29th 2023 07:19:11 pm                                               #
# Modified   : Wednesday March 29th 2023 09:03:58 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import requests
import json
import time
import re
import os
from datetime import datetime
import logging

from urllib.parse import quote_plus

from aimobile.scraper.base import AppData, AppReviews
from aimobile.services.io import IOService


# ------------------------------------------------------------------------------------------------ #
class AppstoreData(AppData):
    """Encapsulates data scraped from the appstore.

    Args:
        directory (str): The home directory into which app data will be stored.
        io (IOService): The file reader and writer.
    """

    # Scrape parameters
    __max_results = 200
    __sleep_min = 5
    __sleep_max = 20

    def __init__(
        self,
        directory: str = "data/appstore/app_data/",
        io: IOService = IOService,
        mock: bool = False,
    ) -> None:
        self._directory = directory
        self._io = io
        self._mock = mock
        self._sleep_min = AppstoreData.__sleep_min
        self._sleep_max = AppstoreData.__sleep_max
        self._max_results = AppstoreData.__max_results

        self._logging = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def scrape(self, category: str) -> None:
        """Scrapes data for the category and saves it as a pandas dataframe in the designated directory.

        The filename is of the format <category>_data.json.

        Args:
            category (str): Single word search term for the category of interest.

        """

    def read(self, category: str) -> pd.DataFrame:
        """Returns the app data for the designated category

        Args:
            category (str): Single word search term for the category of interest.
        """

    def write(self, data: pd.DataFrame, category: str) -> None:
        """Saves the app data to file.

        Args:
            data (pd.DataFrame): Dataframe containing the app data.
            category (str): The category of the data

        """

    def summary(self) -> None:
        """Prints a summary of app scrapes."""
