#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/app_store.py                                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 12:41:54 pm                                                  #
# Modified   : Wednesday March 29th 2023 06:07:24 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
from dotenv import load_dotenv
import logging
import time
import random

import pandas as pd
from serpapi import GoogleSearch
from tqdm import tqdm
from IPython.display import HTML

from aimobile.services.io import IOService
from aimobile.data.base import Scraper


# ------------------------------------------------------------------------------------------------ #
class AppstoreScraper(Scraper):
    """Scrapes Appstore App Data.

    Args:
        max_results (int): Number of results per page. Default = 200
        max_pages (int): Default number of pages to return.
        directory (str): The home directory for data.
        io (IOService): The file reader and writer.
        sleep_min (int): The minimum number of seconds between requests.
        sleep_max (int): The maximum number of seconds between requests.
        mock (bool): Whether to mock the request. Used for testing.
    """

    __summary_filepath = "data/apple/summary.pkl"
    __PARAMS = {
        "engine": "apple_app_store",
        "term": None,
        "country": "us",
        "lang": "en-us",
        "num": "200",
        "page": 0,
        "no_cache": "true",
        "device": "mobile",
        "api_key": None,
    }
    __mock_filepath = "data/apple/medical.json"

    def __init__(
        self,
        max_results: int = 200,
        max_pages: int = 10,
        directory: str = "data/apple/appdata/",
        io: IOService = IOService,
        sleep_min: int = 10,
        sleep_max: int = 20,
        mock: bool = False,
    ) -> None:
        self._max_results = max_results
        self._max_pages = max_pages
        self._directory = directory
        self._io = io
        self._sleep_min = sleep_min
        self._sleep_max = sleep_max
        self._mock = mock

        self._data = {}
        self._logging = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    @property
    def data(self) -> dict:
        return self._data

    def scrape(self, category: str, page: int = None, directory: str = None) -> None:
        """Scrapes app data for the category and saves it in the designated directory.

        The filename is of the format <category_page_num>.py.

        Args:
            category (str): Single word search term for the category of interest.
            page (int): The page to scrape. Optional. Default first max_pages pages.
            directory (str): Optional. Defaults to the directory designated in the constructor.

        """
        load_dotenv()
        params = AppstoreScraper.__PARAMS
        params["term"] = category
        params["num"] = self._max_results
        params["api_key"] = os.getenv("SERPAPI_APIKEY")
        if page is None:
            self._scrape_pages(params=params, category=category, directory=directory)
        else:
            self._scrape_page(params=params, category=category, page=page, directory=directory)

    def load(self, category: str, page: int = 0, directory: str = None) -> None:
        """Loads app data for the designated category and page into the data attribute.

        Args:
            category (str): Single word search term for the category of interest.
            page (int): The page number for the category results
            directory (str): The directory into which the file shall be saved. Optional.
                Defaults to the directory established at object construction.
        """
        directory = directory or self._directory
        filename = category + "_" + str(page) + ".json"
        filepath = os.path.join(directory, filename)
        self._data = IOService.read(filepath=filepath)

    def save(self, data: dict, category: str, page: int, directory: str = None) -> None:
        """Saves the app data to file.

        Args:
            data (dict): Dictionary containing the app data.
            category (str): The category of the data
            page (int): The page number of the results
            directory (str): The directory into which the file shall be saved. Optional.
                Defaults to the directory established at object construction.

        """
        directory = directory or self._directory
        filename = category + "_" + str(page) + ".json"
        filepath = os.path.join(directory, filename)
        IOService.write(filepath=filepath, data=data)
        self._register(category=category, page=page, filepath=filepath)

    def summary(self) -> None:
        """Prints a summary of app scrapes."""
        summary = IOService.read(AppstoreScraper.__summary)
        df = pd.DataFrame(summary)
        HTML(df.to_html(classes="table table-stripped"))

    def _scrape_page(self, params: dict, category: str, page: int, directory: str) -> None:
        params["page"] = page
        results = self._scrape(params)
        self.save(data=results, category=category, page=page, directory=directory)
        self._logger.info(f"Scraped {category} category page {page}.")

    def _scrape_pages(self, params: dict, category: str, directory: str) -> None:
        """Scrapes all pages up to a maximum of max_pages pages."""

        for page in tqdm(range(self._max_pages)):
            params["page"] = page
            results = self._scrape(params=params)
            self.save(data=results, category=category, page=page, directory=directory)
            self._logger.info(f"Scraped {category} category page {page}.")
            if not results["serpapi_pagination"].get("next", None):
                break
            delay = random.randint(a=self._sleep_min, b=self._sleep_max)
            time.sleep(delay)

    def _scrape(self, params: dict) -> dict:
        if self._mock:
            return self._io.read(filepath=AppstoreScraper.__mock_filepath)
        else:
            search = GoogleSearch(params)
            return search.get_dict()

    def _register(self, category: str, page: int, filepath: str) -> None:
        try:
            df = self._io.read(AppstoreScraper.__summary_filepath)
        except Exception:
            df = pd.DataFrame()
        d = {
            "scraper": self.__class__.__name__,
            "site": self._params.get("engine"),
            "category": category,
            "page": page,
            "filepath": filepath,
        }
        df2 = pd.DataFrame(data=d, index=df.shape[0])
        df = pd.concat([df, df2], axis=0)
        IOService.write(filepath=AppstoreScraper.__summary_filepath, data=df)
