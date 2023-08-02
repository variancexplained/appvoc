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
# Modified   : Wednesday August 2nd 2023 01:49:41 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Review Request Module"""
from __future__ import annotations
import sys
import logging

from dependency_injector.wiring import Provide, inject

from appstore.infrastructure.web.headers import STOREFRONT
from appstore.data.acquisition.base import Scraper, App
from appstore.data.acquisition.review.validator import ReviewValidator
from appstore.data.acquisition.review.result import ReviewResult
from appstore.container import AppstoreContainer
from appstore.infrastructure.web.session import SessionHandler


# ------------------------------------------------------------------------------------------------ #
class ReviewScraper(Scraper):
    """App Store Review Scraper"""

    @inject
    def __init__(
        self,
        app: App,
        session_handler: SessionHandler = Provide[AppstoreContainer.web.session],
        start: int = 0,
        max_results_per_page: int = 400,
        max_pages: int = sys.maxsize,
        failure_threshold: int = 5,
    ) -> None:
        self._app = app
        self._session_handler = session_handler
        self._start_index = start
        self._end_index = start + max_results_per_page
        self._max_results_per_page = max_results_per_page
        self._max_pages = max_pages
        self._failure_threshold = failure_threshold

        self._page = 0
        self._failure_count = 0
        self._header = STOREFRONT["headers"]

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def __iter__(self) -> ReviewScraper:
        return self

    def __next__(self) -> ReviewScraper:
        """Formats an itunes request for the next page"""

        if self._page < self._max_pages:
            url = self._setup_url()

            validator = ReviewValidator()
            result = ReviewResult()

            while self._failure_count < self._failure_threshold:
                response = self._session_handler.get(url=url, header=self._header)
                if validator.is_valid(response=response):
                    self._failure_count = 0
                    result.add_response(response=response, app=self._app)
                    self._paginate_url()
                    return result
                elif validator.client_error or validator.server_error:
                    self._failure_count += 1
                    self._paginate_url()

            raise StopIteration
        else:
            raise StopIteration

    def _setup_url(self) -> None:
        """Sets the request url"""
        return f"https://itunes.apple.com/WebObjects/MZStore.woa/wa/userReviewsRow?id={self._app.id}&displayable-kind=11&startIndex={self._start_index}&endIndex={self._end_index}&sort=1"

    def _paginate_url(self) -> None:
        self._page += 1
        self._start_index += self._max_results_per_page  # results
        self._end_index += self._max_results_per_page
        self._setup_url()
