#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Fileapp_name   : /aimobile/scraper/appstore/http/review.py                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 10th 2023 05:01:05 am                                                  #
# Modified   : Wednesday April 19th 2023 04:44:37 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Review Request Module"""
from __future__ import annotations
import logging

import requests
import pandas as pd

from aimobile.data.x_appstore.http.base import RequestIterator, Handler, HTTPVars
from aimobile.data.x_appstore.http.base import HEADERS


# ------------------------------------------------------------------------------------------------ #
class AppStoreReviewRequest(RequestIterator):
    def __init__(
        self,
        app_id: int,
        app_name: str,
        category_id: int,
        category: str,
        handler: Handler,
        page: int = 1,
        max_pages: int = HTTPVars.MAX_PAGES,
    ) -> None:
        self._app_id = app_id  # App id
        self._app_name = app_name
        self._category_id = category_id
        self._category = category
        self._handler = handler
        self._page = page
        self._max_pages = max_pages
        self._pages = 0
        self._results = 0

        self._params = {}
        self._status_code = None
        self._result = None

        self._host = "itunes.apple.com"
        self._url = None
        self._params = None
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    @property
    def host(self) -> int:
        """Returns the current page processed."""
        return self._host

    @property
    def url(self) -> int:
        """Returns the current page processed."""
        return self._url

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
    def result(self) -> int:
        """Returns result in DataFrame format."""
        return self._result

    def __iter__(self) -> AppStoreReviewRequest:
        self._setup()
        return self

    def __next__(self) -> None:
        """Formats an itunes request for the next page"""
        if self._pages < self._max_pages:
            session = self._handler.get(url=self._url, params=self._params, headers=HEADERS)

            if self._is_valid_response(session):
                response = self._parse_session(session)
                self._result = self._parse_response(response)
                self._pagenate_url()
                return self
            else:
                msg = f"Invalid response: \n{response.json()}"
                self._logger.debug(msg)
                self._teardown()
                return self
        else:
            self._teardown()
            return self

    def _setup(self) -> None:
        """Initializes the iterator"""
        self._pages = 0
        self._results = 0
        self._status_code = None
        self._result = None
        self._set_url()

    def _teardown(self) -> None:
        msg = f"Executing teardown on app id: {self._app_id}."
        self._logger.info(msg)
        self._status_code = HTTPVars.DONE
        raise StopIteration

    def _set_url(self) -> None:
        """Sets the initial request url"""
        self._url = f"http://itunes.apple.com/us/rss/customerreviews/id={self._app_id}/sortBy=mostHelpful/json"

    def _pagenate_url(self) -> None:
        """Sets the URL to retrieve the next page."""
        self._page += 1
        self._pages += 1
        self._url = f"http://itunes.apple.com/us/rss/customerreviews/page={self._page}/id={self._app_id}/sortby=mosthelpful/json"

    def _parse_response(self, response: requests.Response) -> pd.DataFrame:
        """Accepts a requests Response object and returns a DataFrame

        Args:
            response (requests.Response): A requests Response object.

        """
        result_list = []
        try:
            results = response.json()["feed"]["entry"]

            for result in results:
                review = {}
                review["id"] = int(result["id"]["label"])
                review["app_id"] = self._app_id
                review["app_name"] = self._app_name
                review["category_id"] = self._category_id
                review["category"] = self._category
                review["author"] = result["author"]["name"]["label"]
                review["rating"] = int(result["im:rating"]["label"])
                review["title"] = result["title"]["label"]
                review["content"] = result["content"]["label"]
                review["vote_sum"] = int(result["im:voteSum"]["label"])
                review["vote_count"] = int(result["im:voteCount"]["label"])
                review["date"] = result["updated"]["label"]
                review["source"] = self._host
                result_list.append(review)

            df = pd.DataFrame(data=result_list)
            self._results = df.shape[0]
            return df
        except requests.exceptions.JSONDecodeError:
            return pd.DataFrame()

    def _parse_session(self, session: Handler) -> requests.Response:
        """Extracts data from the sesion object"""
        self._status_code = int(session.response.status_code)
        return session.response

    def _is_valid_response(self, session: Handler) -> bool:
        """Returns True if an requests.Response object was returned."""
        try:
            response = session.response
            results = response.json()
            return (
                session.status_code == 200
                and isinstance(response, requests.Response)
                and "feed" in results
                and "entry" in results["feed"]
                and isinstance(results["feed"]["entry"], list)
            )
        except Exception:
            return False
