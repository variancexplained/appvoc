#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /aimobile/data/acquisition/appdata/scraper.py                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 04:38:40 am                                                 #
# Modified   : Thursday June 1st 2023 11:16:31 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module containing command objects which encapsulate requests and response processing."""
from __future__ import annotations
import requests
import logging
import sys
from datetime import datetime

import pandas as pd
from dependency_injector.wiring import Provide, inject

from aimobile.data.acquisition.base import Scraper
from aimobile.data.acquisition.appdata.result import AppDataResult
from aimobile.infrastructure.web.session import SessionHandler
from aimobile.container import AIMobileContainer


# ------------------------------------------------------------------------------------------------ #
#                            APPSTORE APP DATA SCRAPER                                             #
# ------------------------------------------------------------------------------------------------ #
class AppDataScraper(Scraper):
    """App Store App Scraper

    Args:
        session (Handler): Handles the session that performs the request, managing
            retries as defined in the session session object.

    """

    __scheme = "https"
    __host = "itunes.apple.com"
    __command = "search?"
    __media = "software"
    __country = "us"
    __explicit = "yes"
    __lang = "en-us"
    __limit = 200
    __max_pages = sys.maxsize

    @inject
    def __init__(
        self,
        term: str,
        session: SessionHandler = Provide[AIMobileContainer.web.session],
        start_page: int = 0,
        limit: int = 200,
        max_pages: int = sys.maxsize,
    ) -> None:
        super().__init__()
        self._page = start_page
        self._term = term
        self._session = session
        self._limit = limit or self.__limit
        self._max_pages = max_pages or self.__max_pages

        self._pages = 0
        self._results = 0
        self._url = None
        self._params = None
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def __iter__(self) -> AppDataScraper:
        self._setup()
        return self

    def __next__(self) -> AppDataResult:
        """Formats an itunes request for the next page"""
        if self._pages < self._max_pages:
            self._set_next_url()
            session = self._session.get(url=self._url, params=self._params)
            try:
                if self._is_valid_response(session=session):
                    self._pages += 1  # Increment page count prior to result and page after.
                    result = self._parse_response(session.response)
                    self._page += 1
                    return result
                else:  # pragma: no cover
                    raise StopIteration

            except requests.exceptions.JSONDecodeError as e:  # pragma: no cover
                msg = f"Encountered {type[e]} exception. Likely a Nonetype exception on the session. Implying 204. Returning to calling environment. Details\n{e}"
                self._logger.error(msg)
                self._status_code = 204
                raise StopIteration
        else:
            raise StopIteration

    def _setup(self) -> None:
        """Initializes the iterator"""
        self._pages = 0
        self._results = 0
        self._status_code = None
        self._url = f"{self.__scheme}://{self.__host}/{self.__command}"

        self._params = {
            "media": self.__media,
            "term": self._term,
            "country": self.__country,
            "lang": self.__lang,
            "explicit": self.__explicit,
            "limit": self._limit,
            "offset": self._page * self._limit,
        }

    def _is_valid_response(self, session: SessionHandler) -> bool:  # pragma: no cover
        """Returns True if response is valid, False otherwise.

        Args:
            session (SessionHandler): Session Handler object

        """
        valid = True
        results = []
        if session.status_code != 200:
            msg = f"\nInvalid status code={session.status_code} encountered. Terminating at page {self._page}."
            valid = False
            self._logger.error(msg)
            return valid
        else:
            try:
                results = session.response.json()["results"]
            except AttributeError as e:
                msg = f"\n{e}. Terminating at page {self._page}."
                valid = False
                self._logger.error(msg)
                return valid
            except KeyError as e:
                msg = f"\nInvalid response encountered. Response has no 'results' key.\n{e}\nTerminating at page {self._page}."
                valid = False
                self._logger.error(msg)
                return valid

        if not isinstance(results, list):
            msg = f"\nInvalid response encountered. Result data type not expected. Terminating at page {self._page}."
            valid = False
            self._logger.error(msg)
            return valid

        if len(results) == 0:
            valid = False
            msg = f"\nInvalid Response: Zero length result encountered. Terminating at page {self._page}."
            self._logger.error(msg)
            return valid

        return valid

    def _parse_response(self, response: requests.Response) -> pd.DataFrame:
        """Accepts a requests Response object and returns a DataFrame

        Args:
            response (requests.Response): A requests Response object.

        """
        result_list = []
        results = response.json()["results"]
        for result in results:
            appdata = {}
            appdata["id"] = result["trackId"]
            appdata["name"] = result["trackName"]
            appdata["description"] = result["description"].strip()
            appdata["category_id"] = result["primaryGenreId"]
            appdata["category"] = result["primaryGenreName"]
            appdata["price"] = result.get("price", 0)
            appdata["developer_id"] = result["artistId"]
            appdata["developer"] = result["artistName"]
            appdata["rating"] = result["averageUserRating"]
            appdata["ratings"] = result["userRatingCount"]
            appdata["rating_current_version"] = result["averageUserRatingForCurrentVersion"]
            appdata["ratings_current_version"] = result["userRatingCountForCurrentVersion"]
            appdata["released"] = datetime.strptime(result["releaseDate"], "%Y-%m-%dT%H:%M:%f%z")
            appdata["released_current"] = datetime.strptime(
                result["currentVersionReleaseDate"], "%Y-%m-%dT%H:%M:%f%z"
            )
            appdata["version"] = result["version"]
            result_list.append(appdata)
        df = pd.DataFrame(data=result_list)

        result = AppDataResult(
            scraper=type[self],
            page=self._page,
            pages=self._pages,
            size=response.headers.get("content-length", 0),
            results=len(df),
            content=df,
        )
        self._results = len(df)

        return result

    def _set_next_url(self) -> None:
        """Sets the parameter variable for the next url."""
        self._params["offset"] += self._results
