#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/review/scraper.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 05:20:01 pm                                                  #
# Modified   : Sunday July 30th 2023 06:00:29 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Review Request Module"""
from __future__ import annotations
import sys
import logging

import requests
from dependency_injector.wiring import Provide, inject

from appstore.infrastructure.web.headers import STOREFRONT
from appstore.data.acquisition.base import Scraper
from appstore.data.acquisition.review.result import ReviewResponse, ReviewResult
from appstore.container import AppstoreContainer
from appstore.infrastructure.web.session import SessionHandler


# ------------------------------------------------------------------------------------------------ #
class ReviewScraper(Scraper):
    """App Store Review Scraper"""

    @inject
    def __init__(
        self,
        app_id: int,
        app_name: str,
        category_id: int,
        category: str,
        session: SessionHandler = Provide[AppstoreContainer.web.session],
        start: int = 0,
        max_results_per_page: int = 400,
        max_pages: int = sys.maxsize,
        failure_threshold: int = Provide[AppstoreContainer.config.web.scraper.failures_threshold],
    ) -> None:
        self._app_id = app_id
        self._app_name = app_name
        self._category_id = category_id
        self._category = category
        self._session = session
        self._start = start
        self._max_results_per_page = max_results_per_page
        self._max_pages = max_pages
        self._failure_threshold = failure_threshold

        self._page = 0
        self._result = None
        self._failure_count = 0

        self._start_index = start
        self._end_index = start + max_results_per_page
        self._url = None
        self._header = STOREFRONT["headers"]

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def result(self) -> ReviewResult:
        return self._result

    def __iter__(self) -> ReviewScraper:
        return self

    def __next__(self) -> ReviewScraper:
        """Formats an itunes request for the next page"""

        if self._page < self._max_pages:
            self._setup_url()

            response = self._session.get(url=self._url, header=self._header)
            self._result = self._parse_response(response)
            if self._failure_count < self._failure_threshold:
                self._paginate_url()
                return self
            else:
                raise StopIteration

    def _setup_url(self) -> None:
        """Sets the header iterable and request url"""
        msg = f"\nSetting URL for App: {self._app_id}-{self._app_name}  URL: Start Index: {self._start_index} End Index: {self._end_index}."
        self._logger.debug(msg)
        self._url = f"https://itunes.apple.com/WebObjects/MZStore.woa/wa/userReviewsRow?id={self._app_id}&displayable-kind=11&startIndex={self._start_index}&endIndex={self._end_index}&sort=1"

    def _is_valid_response(self, response: requests.Response) -> bool:
        """Evaluates response status code and content"""
        valid = True

        try:
            if response.headers.status_code != 200:
                msg = f"Invalid Response: Status code = {response.headers.status_code}."
                valid = False
            elif not isinstance(response, requests.Response):
                msg = f"Invalid Response: Response is of type {type(response)}."
                valid = False
            elif not isinstance(response.json(), dict):
                msg = f"Invalid Response: Response json is of type {type(response.json())}."
                valid = False
            elif "userReviewList" not in response.json():
                msg = "Invalid Response: Response json has no 'userReviewList' key."
                valid = False
            elif not isinstance(response.json()["userReviewList"], list):
                msg = f"Invalid Response: Response json 'userReviewList' is of type {type(response.json()['userReviewList'])}, not a list."
                valid = False
            elif len(response.json()["userReviewList"]) == 0:
                msg = "Invalid Response: Response json 'userReviewList' has zero length."
                valid = False

        except Exception as e:
            valid = False
            msg = f"Invalid Response. A {type(e)} exception occurred. \n{e}"

        if not valid:
            self._logger.debug(msg)
        return valid

    def _parse_response(self, response: requests.Response) -> ReviewResult:
        review_result = ReviewResult()

        if self._is_valid_response(response=response):
            self._failure_count = 0

            for result in response.json()["userReviewList"]:
                review_response = ReviewResponse.create(
                    app_id=self._app_id,
                    app_name=self._app_name,
                    category_id=self._category_id,
                    category=self._category,
                    response=result,
                )
                review_result.update_result(response=review_response)
        else:
            self._failure_count += 1
            review_result.requests += 1
            review_result.fails += 1

        return review_result

    def _paginate_url(self) -> None:
        self._page += 1
        self._start_index += self._max_results_per_page  # results
        self._end_index += self._max_results_per_page
        self._setup_url()
