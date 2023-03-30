#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/appstore/scraper/app_data.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday March 29th 2023 07:19:11 pm                                               #
# Modified   : Thursday March 30th 2023 07:40:13 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import print_function
import requests
import time
import os
from datetime import datetime
import logging
import random
from dataclasses import dataclass

from dependency_injector.wiring import Provide, inject
from IPython.display import HTML
import pandas as pd

from aimobile.data.appstore.scraper.base import (
    AppData,
    AppStoreResults,
    AppStoreParams,
)

URLFORMAT = "https://itunes.apple.com/search?media=software&term=Health&country=us&lang=en-us&explicit=yes&limit=200&offset=0"


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppStoreScrapeParams:
    category: str
    max_pages: int = None
    page_size: int = None
    timeout: int = None
    sleep_min: int = None
    sleep_max: int = None
    base_url: str = "https://itunes.apple.com/search?"
    media: str = "software"
    country: str = "us"
    lang = "en-us"
    explicit = "yes"
    request_id = None

    def __post_init__(self) -> None:
        self.max_pages = self.max_pages or AppStoreParams.max_pages
        self.page_size = self.page_size or AppStoreParams.page_size
        self.timeout = self.timeout or AppStoreParams.timeout
        self.sleep_min = self.sleep_min or AppStoreParams.sleep_min
        self.sleep_max = self.sleep_max or AppStoreParams.sleep_max
        self.request_id = self.category + "_0"


# ------------------------------------------------------------------------------------------------ #
class AppStoreData(AppData):
    """Encapsulates data scraped from the appstore.

    Args:
        appdata (SqliteDatabase): Database containing app data.
        registry (SqliteDatabase): Database containing the registry
    """

    def __init__(
        self,
        appdata: str = None,
        mock: bool = False,
    ) -> None:
        self._directory = directory or AppStoreData.__directory
        self._app_data_db_location = "sqlite:///" + os.path.join(self._directory, "app_data.db")
        self._app_data_registry_db_location = "sqlite:///" + os.path.join(
            self._directory, "app_data_registry.db"
        )

        self._mock = mock

        self._app_data_db = sqlalchemy.create_engine(self._app_data_db_location)
        self._app_data_registry_db = sqlalchemy.create_engine(self._app_data_registry_db_location)

        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def scrape(self, params: AppStoreScrapeParams) -> None:
        """Scrapes the data according to the parameters in the AppStoreScrapeParams object.

        Args:
            params (AppStoreScrapeParams): Scrape parameter object

        """
        self._logger.info(f"Scraping {params.category} category from the App Store")
        category_data = None
        pages = 0

        filepath = self._get_filepath(category=params.category)
        request_params = self._initialize_request_params(params=params)
        registry = self._initialize_registry(category=params.category, filepath=filepath)
        headers = self._get_headers(params=params)

        while True:

            if pages >= params.max_pages:
                break

            response = self._scrape_page(
                url=params.base_url, params=request_params, headers=headers, timeout=params.timeout
            )

            if response.status_code == 200:
                print(".", end="", flush=True)
                pages += 1

                # Extract results
                results = response.json()

                # Extract the data of interest from page results and return a dataframe.
                page_data = self._parse_results(results=results, request_params=request_params)

                # Add page data to database.
                page_data.to_sql(name="app_data", con=self._)
                category_data = self._update_category_data(
                    page_data=page_data, category_data=category_data
                )

                # Increment the offset in the request params
                request_params = self._update_request_params(request_params)

                # Update the registry with the number of pages and apps returned
                registry = self._update_registry(registry=registry, results=results)

                # Delay to prevent overloading servers with requests.
                self._delay(params)
            else:
                break

        # write the app data for the category
        self.write(data=category_data, filepath=registry.get("filepath"))

        # Add the category to the registry
        self._register_category(registry=registry)

        msg = f"Scraped {registry['apps']} from the {registry['category']} category."
        self._logger.info(msg)

    def read(self, category: str) -> pd.DataFrame:
        """Returns the app data for the designated category

        Args:
            category (str): Single word search term for the category of interest.
        """
        filepath = self._get_filepath(category=category)
        try:
            return self._io.read(filepath=filepath)
        except FileNotFoundError:
            msg = f"No data found for {category} category"
            self._logger.error(msg)
            raise ValueError(msg)

    def write(self, data: pd.DataFrame, filepath: str) -> None:
        """writes the app data to file.

        Args:
            data (pd.DataFrame): Dataframe containing the app data.
            category (str): The category of the data

        """
        self._io.write(filepath=filepath, data=data)

    def summary(self) -> None:
        """Prints a summary of app scrapes."""

        try:
            registry = self._io.read(filepath=self._registry_filepath)
            df = pd.DataFrame(data=registry)
            print(HTML(df.to_html(classes="table table-stripped")))
        except FileNotFoundError:
            print("No data exists")

    def _scrape_page(self, url: str, params: dict, headers: dict, timeout: int) -> dict:
        """Scrapes the data from the appstore and returns a dictionary

        Args:
            url: The base url to send to requests.get
            params (dict): The parameters to send to requests.get
            headers (dict): Request header
            timeout (int): Seconds before an timeout HTTPError is raised.
        """
        try:
            return requests.get(url=url, params=params, headers=headers, timeout=timeout)
        except requests.exceptions.Timeout as e:  # pragma: no cover
            msg = f"Error scraping {url}. Query timed out. Response code: {e.response.status_code}.\nDetails: {e}"
            self._logger.error(msg)
            raise e
        except requests.exceptions.HTTPError as e:  # pragma: no cover
            msg = f"Error scraping {url}. Response code: {e.response.status_code}.\nDetails: {e}"
            self._logger.error(msg)
            raise e
        except requests.exceptions.ConnectionError:
            self._delay()
            self._scrape_page(url=url, params=params, headers=headers, timeout=timeout)

    def _parse_results(self, results: dict, request_params: dict) -> pd.DataFrame:
        """Extracts data of interest from a page of results into a pandas DataFrame"""
        page_data = []
        app_data = {}

        # Extract data of interest into a list of dictionaries.
        for result in results["results"]:
            for key, result_key in AppStoreResults.map.items():
                app_data[key] = result.get(result_key, None)
            app_data["request_id"] = (
                request_params.get("category") + _ + str(request_params.get("offset"))
            )
            page_data.append(app_data)

        # Convert the list of dictionaries into a pandas DataFrame and return it.
        return pd.DataFrame(data=page_data)

    def _update_category_data(
        self, page_data: pd.DataFrame, category_data: pd.DataFrame = None
    ) -> pd.DataFrame:
        """Adds the app_data from the request to the category_data dataframe"""
        if category_data is not None:
            category_data = pd.concat([category_data, page_data], axis=0)
        else:
            category_data = page_data
        return category_data

    def _initialize_request_params(self, params: AppStoreScrapeParams) -> dict:
        """Initializes the parameters for requests.get"""
        request_params = {}
        request_params["media"] = params.media
        request_params["country"] = params.country
        request_params["lang"] = params.lang
        request_params["explicit"] = params.explicit
        request_params["term"] = params.category
        request_params["limit"] = params.page_size
        request_params["offset"] = 0
        request_params["request_id"] = params.request_id
        return request_params

    def _update_request_params(self, request_params: dict) -> dict:
        """Updates the parameter object for each iteration"""
        request_params["offset"] += 1
        request_params["request_id"] = (
            request_params["category"] + "_" + str(request_params["offset"])
        )
        return request_params

    def _initialize_registry(self, category: str, filepath: str) -> dict:
        """Initializes the registry for the category"""
        return {
            "site": "itunes.apple.com",
            "scraper": self.__class__.__name__,
            "category": category,
            "pages": 0,
            "apps": 0,
            "filepath": filepath,
            "created": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        }

    def _update_registry(self, registry: dict, results: dict) -> dict:
        """Updates the registry with the number of pages and apps"""
        registry["pages"] += 1
        registry["apps"] += results.get("resultCount")
        return registry

    def _get_filepath(self, category: str) -> str:
        """Returns the filepath into which the category app data will be stored."""
        filename = "appdata.pkl"
        return os.path.join(self._directory, category, filename)

    def _delay(self, params: AppStoreScrapeParams) -> None:
        """Delays a random number of seconds between min and max delay."""
        delay = random.randint(a=params.sleep_min, b=params.sleep_max)
        time.sleep(delay)

    def _register_category(self, registry: dict) -> None:
        """Register the category"""
        registry_data = None
        try:
            registry_data = self._io.read(filepath=self._registry_filepath)
        except FileNotFoundError:
            pass

        if registry_data is None:
            registry_data = [registry]
        else:
            registry_data.append(registry)

        self._io.write(filepath=self._registry_filepath, data=registry_data)

    def _get_headers(self, params: dict) -> dict:
        """Returns the header for the next request."""
        return {"X-Apple-Store-Front": "143441-1,29", "Accept-Language": params.lang}
