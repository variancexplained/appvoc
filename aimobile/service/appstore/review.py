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
# Modified   : Saturday April 22nd 2023 04:22:56 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Review Request Module"""
from __future__ import annotations
import sys
import logging
from datetime import datetime

import requests
import pandas as pd
from dependency_injector.wiring import Provide, inject

from aimobile.service.base import ReviewScraper
from aimobile.infrastructure.web.base import STOREFRONTS
from aimobile.container import AIMobileContainer
from aimobile.infrastructure.web.session import SessionHandler


# ------------------------------------------------------------------------------------------------ #
class AppStoreReviewScraper(ReviewScraper):
    """App Store Review Scraper"""

    @inject
    def __init__(
        self,
        app_id: int,
        app_name: str,
        category_id: int,
        category: str,
        session: SessionHandler = Provide[AIMobileContainer.web.session],
        start: int = 0,
        max_results_per_page: int = 400,
        max_pages: int = sys.maxsize,
    ) -> None:
        self._app_id = app_id
        self._app_name = app_name
        self._category_id = category_id
        self._category = category
        self._session = session
        self._start = start
        self._max_results_per_page = max_results_per_page
        self._max_pages = max_pages

        self._page = 0
        self._result = None
        self._results = 0

        self._status_code = None
        self._start_index = start
        self._end_index = start + max_results_per_page
        self._host = "itunes.apple.com"
        self._url = None
        self._header = STOREFRONTS[0]["headers"]

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

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
    def page(self) -> int:
        """Returns the current page processed."""
        return self._page

    @property
    def results(self) -> int:
        """Returns the number of results returned."""
        return self._results

    @property
    def result(self) -> int:
        """Returns result in DataFrame format."""
        return self._result

    def __iter__(self) -> AppStoreReviewScraper:
        return self

    def __next__(self) -> None:
        """Formats an itunes request for the next page"""

        if self._page < self._max_pages:
            self._setup_url()

            session = self._session.get(url=self._url, header=self._header)

            if self._is_valid_response(session):
                response = self._parse_session(session)
                self._result = self._parse_response(response)
                self._paginate_url()
                return self
            else:
                raise StopIteration
        else:  # pragma: no cover
            raise StopIteration

    def _setup_url(self) -> None:
        """Sets the request url"""
        msg = f"\nSetting URL for App: {self._app_id}-{self._app_name}  URL: Start Index: {self._start_index} End Index: {self._end_index}."
        self._logger.debug(msg)
        self._url = f"https://itunes.apple.com/WebObjects/MZStore.woa/wa/userReviewsRow?id={self._app_id}&displayable-kind=11&startIndex={self._start_index}&endIndex={self._end_index}&sort=1"

    def _is_valid_response(self, session: SessionHandler) -> bool:
        """Evaluates response status code and content"""
        valid = (
            session.status_code == 200
            and isinstance(session.response, requests.Response)
            and isinstance(session.response.json()["userReviewList"], list)
            and len(session.response.json()["userReviewList"]) > 0
        )

        if not valid:
            len_result = len(session.response.json()["userReviewList"])
            type_result = type(session.response.json()["userReviewList"])
            msg = f"\n\nInvalid response encountered for:\n\tApp: {self._app_id}-{self._app_name}\n\tPages: {self._page}\n\tStart Index: {self._start_index}\n\tEnd Index: {self._end_index}\n\tStatus Code: {session.status_code}\n\tLength Result: {len_result}\n\tType Result: {type_result}"
            self._logger.debug(msg)
        return valid

    def _parse_response(self, response: requests.Response) -> pd.DataFrame:
        """Accepts a requests Response object and returns a DataFrame

        Args:
            response (requests.Response): A requests Response object.

        """
        result_list = []
        try:
            results = response.json()["userReviewList"]

            for result in results:
                review = {}
                review["id"] = result["userReviewId"]
                review["app_id"] = self._app_id
                review["app_name"] = self._app_name
                review["category_id"] = self._category_id
                review["category"] = self._category
                review["author"] = result["name"]
                review["rating"] = int(result["rating"])
                review["title"] = result["title"]
                review["content"] = result["body"]
                review["vote_sum"] = int(result["voteSum"])
                review["vote_count"] = int(result["voteCount"])
                review["date"] = datetime.strptime(result["date"], "%Y-%m-%dT%H:%M:%f%z")
                review["source"] = self._host
                result_list.append(review)

            df = pd.DataFrame(data=result_list)
            self._results = df.shape[0]
            msg = f"\nResults returned: {df.shape[0]}"
            self._logger.debug(msg)
            return df
        except requests.exceptions.JSONDecodeError:  # pragma: no cover
            return pd.DataFrame()

    def _parse_session(self, session: SessionHandler) -> requests.Response:
        """Extracts data from the sesion object"""
        self._status_code = int(session.response.status_code)
        return session.response

    def _paginate_url(self) -> None:
        self._page += 1
        self._start_index += self._max_results_per_page
        self._end_index += self._max_results_per_page
        self._setup_url()
