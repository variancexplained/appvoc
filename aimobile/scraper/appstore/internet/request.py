#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/internet/request.py                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 04:38:40 am                                                 #
# Modified   : Saturday April 8th 2023 02:45:31 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module containing command objects which encapsulate requests and response processing."""
from __future__ import annotations
import requests
import logging

from dependency_injector.wiring import inject, Provide
import pandas as pd

from aimobile.scraper.appstore.internet.base import RequestIterator, Handler
from aimobile.scraper.appstore.container import AppStoreContainer


# ------------------------------------------------------------------------------------------------ #
class AppStoreSearchRequest(RequestIterator):
    # This is what the formatted url should look like to the target.
    # https://itunes.apple.com/search?media=software&term=Health&country=us&lang=en-us&explicit=yes&limit=10&offset=0/json
    __scheme = "https"
    __host = "itunes.apple.com"
    __command = "search?"
    __media = "software"
    __country = "us"
    __explicit = "yes"
    __lang = "en-us"
    __limit = 200
    __max_pages = 99999

    @inject
    def __init__(
        self,
        term: str,
        limit: int = None,
        max_pages: int = None,
        handler: Handler = Provide[AppStoreContainer.session.handler],
        page: int = 0,
    ) -> None:
        self._term = term
        self._limit = limit or self.__limit
        self._max_pages = max_pages or self.__max_pages
        self._handler = handler
        self._page = page
        self._apps = 0
        self._status = None

        self._url = None
        self._params = None
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    @property
    def pages(self) -> int:
        """Returns the number of pages processed."""
        return self._page

    @property
    def apps(self) -> int:
        return self._apps

    def __iter__(self) -> AppStoreSearchRequest:
        self._apps = 0
        self._url = f"{self.__scheme}://{self.__host}/{self.__command}"
        self._params = {
            "media": self.__media,
            "term": self._term,
            "country": self.__country,
            "lang": self.__lang,
            "explicit": self.__explicit,
            "limit": self._limit,
            "offset": self._page,
        }
        return self

    def __next__(self) -> None:
        """Formats an itunes request for the next page"""
        if self._page < self._max_pages and self._status != 404:
            self._params["offset"] = self._page * self._limit
            response = self._handler.get(url=self._url, params=self._params)
            self._status = response.status_code
            self._page += 1
            result = self.parse_response(response=response)
            self._apps += result.shape[0]
            return result
        else:
            raise StopIteration

    def parse_response(self, response: requests.Response) -> pd.DataFrame:
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
            appdata["description"] = result["description"]
            appdata["category_id"] = result["primaryGenreId"]
            appdata["category"] = result["primaryGenreName"]
            appdata["price"] = result["price"]
            appdata["developer_id"] = result["artistId"]
            appdata["developer"] = result["artistName"]
            appdata["rating"] = result["averageUserRating"]
            appdata["ratings"] = result["userRatingCount"]
            appdata["released"] = result["releaseDate"]
            appdata["source"] = self.__host
            result_list.append(appdata)
        df = pd.DataFrame(data=result_list)
        return df
