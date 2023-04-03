#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/scraper/appstore/service/appdata.py                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday March 30th 2023 07:45:46 pm                                                #
# Modified   : Monday April 3rd 2023 06:26:28 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
import sys
from typing import ClassVar
from types import SimpleNamespace
import requests
import time
from datetime import datetime
from dataclasses import dataclass
import logging
import random
import itertools

import pandas as pd

from aimobile.data.scraper.appstore.service.genera import Scraper, ScrapeParams
from aimobile.data.scraper.base import AbstractAppDataScraper, AbstractScraperProject
from tests.utils.mock import mock_request

# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppStoreDataScraperProject(AbstractScraperProject):
    collection_id: int
    collection: str
    category_id: int
    category: str
    project_id: str = None
    base_url: str = "https://itunes.apple.com/search?"
    media: str = "software"
    country: str = "us"
    lang: str = "en-us"
    explicit: str = "yes"
    offset: int = 0
    limit: int = 200
    max_pages: int = sys.maxsize
    timeout: int = 600
    delay: tuple = (5, 20)
    retries: int = 5
    backoff_base: int = 2

    __id = ClassVar[int] = itertools.count()

    def __post_init__(self) -> None:
        self.project_id = next(AppStoreDataScraperProject.__id)

    @property
    def request_params(self) -> dict:
        """Returns the parameters to be passed to the request method."""
        d = {
            "media": self.media,
            "country": self.country,
            "lang": self.lang,
            "explicit": self.explicit,
            "offset": self.offset,
            "limit": self.limit,
        }
        return d

    @property
    def retries(self) -> SimpleNamespace:
        d = {}


# ------------------------------------------------------------------------------------------------ #
class AppStoreDataScraper(AbstractAppDataScraper):
    """Encapsulates data scraped from the appstore.

    Args:
        repo (AppStoreDataRepo): Repository of App Store data.
    """

    __source = "appstore"
    __datatype = "appdata"

    def __init__(
        self,
        project: AbstractScraperProject,
        mock: bool = False,
    ) -> None:
        self._params = params

        self._mock = mock
        self._project_data = {}  # Project log data
        self._request_data = {}  # Request log data
        self._headers = {}  # HTTP request headers
        self._request_params = {}  # HTTP request params

        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(params={self._params})"

    def __str__(self) -> str:
        width = 12
        return (
            f"{'Source'.rjust(width, ' ')} | {AppStoreDataScraper.__source}\n"
            f"{'Data'.rjust(width, ' ')} | {AppStoreDataScraper.__datatype}\n"
            f"{'Term'.rjust(width, ' ')} | {self._params.term}\n"
            f"{'URL'.rjust(width, ' ')} | {self._params.url}\n"
            f"{'Start Page'.rjust(width, ' ')} | {self._params.offset}\n"
        )

    def scrape(self) -> None:
        """Scrapes the data according to the parameters in the AppStoreScrapeParams object.

        Args:
            params (AppStoreScrapeParams): Scrape parameter object

        """
        self._setup()
        page = 0

        while page < self._params.max_pages:

            # Execute the HTTP request
            response = self.request(
                url=self._params.base_url,
                headers=self._headers,
                params=self._request_params,
                timeout=self._params.timeout,
                retries=self._params.retries,
            )
            if response.status_code == 200:

                # Extract the results from the response object.
                results = response.json()
                # Parse the results and return data of interest as a dataframe.
                appdata = self.parse_results(results=results)
                # Persist the app data to the database
                self._add(data=appdata)
                # Save the project and request log to the database
                self._register(results)
                # Update the request parameters, request log and project for the next request.
                self._set_next_request()
                page += 1
            else:
                break

        self._teardown()

    def summary(self) -> None:
        """Prints a summary of app scrapes."""
        width = 12
        return (
            f"{'Project Id'.rjust(width, ' ')} | {self._project_data['id']}\n"
            f"{'Scraper'.rjust(width, ' ')} | {self._project_data['scraper']}\n"
            f"{'Source'.rjust(width, ' ')} | {AppStoreDataScraper.__source}\n"
            f"{'Data'.rjust(width, ' ')} | {AppStoreDataScraper.__datatype}\n"
            f"{'Term'.rjust(width, ' ')} | {self._project_data['term']}\n"
            f"{'Start Page'.rjust(width, ' ')} | {self._project_data['start_page']}\n"
            f"{'End Page'.rjust(width, ' ')} | {self._project_data['end_page']}\n"
            f"{'Results'.rjust(width, ' ')} | {self._project_data['results']}\n"
            f"{'Stage'.rjust(width, ' ')} | {self._project_data['state']}\n"
            f"{'Started'.rjust(width, ' ')} | {self._project_data['started'].strftime('%m/%d/%Y, %H:%M:%S')}\n"
            f"{'Ended'.rjust(width, ' ')} | {self._project_data['ended'].strftime('%m/%d/%Y, %H:%M:%S')}\n"
            f"{'Duration'.rjust(width, ' ')} | {round(self._project_data['duration'],2)} seconds.\n"
        )

    def _setup(self) -> None:
        """Initial housekeeping"""
        self._initialize_project_data()
        self._initialize_request_data()
        self._initialize_request_params()
        self._initialize_headers()
        self._logger.info(
            f"{self.__class__.__name__} Project: {self._project_data['id']} started.\n\tSource: {self._project_data['source']}\n\tData: {self._project_data['datatype']}\n\tCategory: {self._project_data['term']}"
        )

    def _teardown(self) -> None:
        """Initial housekeeping"""
        self._finalize_project()
        self._register_project()
        self._logger.info(
            f"{self.__class__.__name__} Project: {self._project_data['id']} completed. Duration: {round(self._project_data['duration'],2)} seconds"
        )

    def _request(
        self,
        url: str,
        headers: dict,
        params: dict,
        timeout: int,
        retries: int,
    ) -> requests.Response:
        """Executes an HTTP request with retries if exception."""
        retry = 0
        while retry <= retries:
            try:
                self._delay(retry=retry)
                if self._mock:
                    return mock_request()
                else:
                    return requests.get(url=url, params=params, headers=headers, timeout=timeout)
            except Exception as e:  # pragma: no cover
                retry = self._handle_exception(exception=e, retry=retry, retries=retries)

    def _delay(self, retry: int = 0) -> None:
        """Creates an exponential delay based upon the number of retries."""
        delay = random.randint(*self._params.delay) * self._params.backoff_base**retry
        self._logger.debug(f"Delaying {delay} seconds on attempt {retry}")
        time.sleep(delay)

    def _parse_results(self, results: dict) -> pd.DataFrame:
        """Extracts data of interest from the response, and converts the data to a DataFrame"""
        applist = []
        appdata = {}
        # Extract data of interest into a list of dictionaries.
        for result in results["results"]:
            for key, result_key in AppStoreResults.map.items():
                appdata[key] = result.get(result_key, None)
            appdata["project_id"] = self._project_data["id"]
            appdata["created"] = datetime.now()
            applist.append(appdata)

        # Convert the list of dictionaries into a pandas DataFrame and return it.
        return pd.DataFrame(data=applist)

    def _add(self, data: pd.DataFrame) -> None:
        """Adds the appdata to the database."""
        self._appdata_repo.add(data=data)

    def _register(self, results: dict) -> None:
        """Registers request and the project data"""
        self._update_request_data(results)
        self._update_project_data(results)
        self._register_request()
        self._register_project()

    def _set_next_request(self) -> None:
        self._request_params["offset"] += 1
        self._request_data["page"] += 1
        self._project_data["end_page"] += 1

    def _initialize_project_data(self) -> None:
        """Initializes data that describe the  project"""
        now = datetime.now().strftime("%Y-%m-%d-%H-%M_%S")
        self._project_data[
            "id"
        ] = f"{AppStoreDataScraper.__source}_{AppStoreDataScraper.__datatype}_{self._params.term}_{now}"
        self._project_data["scraper"] = self.__class__.__name__
        self._project_data["source"] = AppStoreDataScraper.__source
        self._project_data["datatype"] = AppStoreDataScraper.__datatype
        self._project_data["term"] = self._params.term
        self._project_data["url"] = self._params.base_url
        self._project_data["start_page"] = self._params.offset
        self._project_data["end_page"] = self._params.offset
        self._project_data["results"] = 0
        self._project_data["started"] = datetime.now()
        self._project_data["ended"] = None
        self._project_data["duration"] = None
        self._project_data["state"] = None

    def _initialize_request_data(self) -> None:
        """Initializes data that is tracked for each request."""
        now = datetime.now().strftime("%Y-%m-%d-%H-%M_%S")
        self._request_data["id"] = f"{AppStoreDataScraper.__datatype}_{self._params.term}_0"
        self._request_data[
            "project_id"
        ] = f"{AppStoreDataScraper.__source}_{AppStoreDataScraper.__datatype}_{self._params.term}_{now}"
        self._request_data["scraper"] = self.__class__.__name__
        self._request_data["source"] = AppStoreDataScraper.__source
        self._request_data["datatype"] = AppStoreDataScraper.__datatype
        self._request_data["term"] = self._params.term
        self._request_data["page"] = self._params.offset
        self._request_data["results"] = 0
        self._request_data["datetime"] = None

    def _initialize_request_params(self) -> None:
        """Initializes the HTTP request parameters"""
        self._request_params["media"] = "software"
        self._request_params["country"] = "us"
        self._request_params["lang"] = "en-us"
        self._request_params["explicit"] = "yes"
        self._request_params["offset"] = 0
        self._request_params["limit"] = 200

    def _initialize_headers(self) -> None:
        self._headers = {"X-Apple-Store-Front": "143441-1,29", "Accept-Language": self._params.lang}

    def _update_request_data(self, results: dict) -> None:
        """Updates the request data at the end of each iteration"""
        self._request_data["results"] = results["resultCount"]
        self._request_data["datetime"] = datetime.now()

    def _update_project_data(self, results: dict) -> None:
        self._project_data["results"] += results["resultCount"]
        self._project_data["ended"] = datetime.now()
        self._project_data["duration"] = (
            self._project_data["ended"] - self._project_data["started"]
        ).total_seconds()
        self._project_data["state"] = self._project_data["state"] or "in_progress"

    def _finalize_project(self) -> None:
        self._project_data["ended"] = datetime.now()
        self._project_data["duration"] = (
            self._project_data["ended"] - self._project_data["started"]
        ).total_seconds()
        self._project_data["state"] = "success"

    def _register_request(self) -> None:
        """Finalizes the request object and adds it to the repository."""
        request_data = pd.DataFrame(self._request_data, index=[0])
        self._repo.register(data=request_data, tablename="request")

    def _register_project(self) -> None:
        """Finalizes the project object and adds it to the repository."""
        project_data_df = pd.DataFrame(data=self._project_data, index=[0])
        self._repo.register(data=project_data_df, tablename="project")

    def _handle_exception(self, exception: Exception, attempt: int, retries: int) -> int:
        """Handles exceptions in the event of retries."""
        attempt += 1
        if attempt >= retries:
            msg = f"Request {self._request_data['request_id']}. Response code: {exception.response.status_code}\n{exception}."
            self._logger.error(msg)
            raise exception
        else:
            msg = f"Request {self._request_data['request_id']}. Response code: {exception.response.status_code}\nRetrying attempt {attempt} of {retries}."
            self._logger.error(msg)
        return attempt


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppStoreScrapeParams(ScrapeParams):
    collection: str  #
    category_id: str
    project_id: str = None
    base_url: str = "https://itunes.apple.com/search?"
    media: str = "software"
    country: str = "us"
    lang: str = "en-us"
    explicit: str = "yes"
    offset: int = 0
    limit: int = 200
    max_pages: int = sys.maxsize
    timeout: int = 600
    delay: tuple = (5, 20)
    retries: int = 5
    backoff_base: int = 2

    def __post_init__(self) -> None:
        self.project_id = self.term + "_" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
