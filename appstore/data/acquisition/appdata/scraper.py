#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/appdata/scraper.py                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 04:38:40 am                                                 #
# Modified   : Tuesday August 29th 2023 09:10:46 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module containing command objects which encapsulate requests and response processing."""
from __future__ import annotations
import logging
import sys

from dependency_injector.wiring import Provide, inject

from appstore.data.acquisition.base import Scraper
from appstore.data.acquisition.appdata.result import AppDataResult
from appstore.data.acquisition.appdata.validator import AppDataValidator
from appstore.infrastructure.web.session import SessionHandler
from appstore.container import AppstoreContainer


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
        session: SessionHandler = Provide[AppstoreContainer.web.session],
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

            validator = AppDataValidator()
            result = AppDataResult()

            response = self._session.get(url=self._url, params=self._params)

            if validator.is_valid(response=response):
                self._page += 1
                self._pages += 1
                result.add_response(response=response, page=self._page, pages=self._pages)
                self._results = result.results
            else:
                result.data_errors += validator.data_error
                result.client_errors += validator.client_error
                result.server_errors += validator.server_error
            return result
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

    def _set_next_url(self) -> None:
        """Sets the parameter variable for the next url."""
        self._params["offset"] += self._results
