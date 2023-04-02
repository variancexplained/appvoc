#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/scrapers/base.py                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 06:29:52 am                                                  #
# Modified   : Friday March 31st 2023 06:34:43 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the abstract base classes for scrapers and repositories."""
from __future__ import annotations
from abc import ABC, abstractmethod

import requests
import pandas as pd


# ------------------------------------------------------------------------------------------------ #
class Scraper(ABC):
    """Abstract base class for scrapers."""

    @abstractmethod
    def scrape(self, params: ScrapeParams) -> None:
        """Controls the scrape process."""

    @abstractmethod
    def summary(self) -> None:
        """Summarizes the scraping project."""

    @abstractmethod
    def _request(self, url: str, headers: dict, params: dict, timeout=int) -> requests.Response:
        """Executes the HTTP request and returns a response object.

        Args:
            url (str): The base url
            headers (dict): The HTTP request headers.
            params (dict): Parameters to be passed to the requests method.
            timeout (int): The time in seconds to receive a response.
            retries (int): The number of HTTP request retries if a request is unsuccessful.
        """

    @abstractmethod
    def _parse_results(self, results: dict) -> pd.DataFrame:
        """Parses the results and returns a DataFrame
        Args:
            results (dict): Results from the HTTP request response object.
        """

    @abstractmethod
    def _add(self, data: pd.DataFrame) -> None:
        """Adds an HTTP response to the database.

        Args:
            data (pd.DataFrame): Response data in DataFrame format.
        """

    @abstractmethod
    def _register(self, results: dict) -> None:
        """Updates the request and project data, then persists the updates  to the database.

        results (dict): Results from the HTTP request response object.
        """


# ------------------------------------------------------------------------------------------------ #
class ScrapeParams(ABC):
    """Base class for scrape parameter objects."""
