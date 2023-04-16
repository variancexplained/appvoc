#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/http/appdata.py                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 04:38:40 am                                                 #
# Modified   : Sunday April 16th 2023 02:19:01 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module containing command objects which encapsulate requests and response processing."""
from __future__ import annotations
import requests
import logging

import pandas as pd

from aimobile.scraper.appstore.http.base import RequestIterator, Handler, HEADERS


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

    def __init__(
        self,
        term: str,
        handler: Handler,
        limit: int = None,
        max_pages: int = None,
        page: int = 0,
    ) -> None:
        self._host = self.__host
        self._term = term
        self._limit = limit or self.__limit
        self._max_pages = max_pages or self.__max_pages
        self._handler = handler
        self._page = page
        self._pages = 0
        self._results = 0
        self._status_code = None
        self._result = None

        self._url = None
        self._params = None
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    @property
    def host(self) -> int:
        """Returns the current page processed."""
        return self.__host

    @property
    def status_code(self) -> int:
        """Returns the length of the response"""
        return self._status_code

    @property
    def term(self) -> int:
        """Returns the search term"""
        return self._term

    @property
    def page(self) -> int:
        """Returns the current page processed."""
        return self._page

    @property
    def pages(self) -> int:
        """Returns the number of pages processed. May not be the same as page if started at nonzero.."""
        return self._pages

    @property
    def results(self) -> int:
        """Returns the number of results returned."""
        return self._results

    @property
    def result(self) -> pd.DataFrame:
        """Returns result in DataFrame format."""
        return self._result

    def __iter__(self) -> AppStoreSearchRequest:
        self._setup()
        return self

    def __next__(self) -> None:
        """Formats an itunes request for the next page"""
        if self._pages < self._max_pages:
            self._set_next_url()
            session = self._handler.get(url=self._url, headers=HEADERS, params=self._params)
            try:
                if session.status_code == 200:
                    response = self._parse_session(session)
                    self._result = self._parse_response(response)
                    self._page += 1
                    self._pages += 1
                    return self
                else:
                    self._teardown()
                    return self

            except requests.exceptions.JSONDecodeError as e:
                msg = f"Encountered {type[e]} exception. Likely a Nonetype exception on the session. Implying 204. Returning to calling environment. Details\n{e}"
                self._logger.error(msg)
                self._status_code = 204
                self._teardown()
                return self
        else:
            self._teardown()
            return self

    def summarize(self) -> None:
        """Prints a summary of the appdata scraping project."""
        print(self._project)

    def _setup(self) -> None:
        """Initializes the iterator"""
        self._pages = 0
        self._results = 0
        self._status_code = None
        self._result = None
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

    def _teardown(self) -> None:
        raise StopIteration

    def _parse_session(self, session: Handler):
        """Extracts data from the sesion object"""
        self._status_code = int(session.response.status_code)
        return session.response

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
            appdata["description"] = result["description"]
            appdata["category_id"] = result["primaryGenreId"]
            appdata["category"] = result["primaryGenreName"]
            appdata["price"] = result.get("price", 0)
            appdata["developer_id"] = result["artistId"]
            appdata["developer"] = result["artistName"]
            appdata["rating"] = result["averageUserRating"]
            appdata["ratings"] = result["userRatingCount"]
            appdata["released"] = result["releaseDate"]
            appdata["source"] = self._host
            result_list.append(appdata)
        df = pd.DataFrame(data=result_list)
        self._results = len(result_list)
        return df

    def _set_next_url(self) -> None:
        """Sets the parameter variable for the next url."""
        self._params["offset"] += self._results
