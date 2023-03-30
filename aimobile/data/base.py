#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/base.py                                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday March 30th 2023 07:09:09 pm                                                #
# Modified   : Thursday March 30th 2023 07:38:14 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the abstract base classes for scrapers and repositories."""
from abc import ABC, abstractmethod
import requests
import pandas as pd


# ------------------------------------------------------------------------------------------------ #
class Registry(ABC):
    """Abstract base class for app data and review registry objects."""


# ------------------------------------------------------------------------------------------------ #
class Scraper(ABC):
    """Abstract base class for scrapers."""

    @abstractmethod
    def scrape(self, *args, **kwargs) -> None:
        """Controls the scrape process."""

    @abstractmethod
    def request(self, url: str, headers: dict, params: dict, timeout=int) -> requests.Response:
        """Executes the HTTP request and returns a response object.

        Args:
            url (str): The base url
            headers (dict): The HTTP request headers.
            params (dict): Parameters to be passed to the requests method.
            timeout (int): The time in seconds to receive a response.
        """

    @abstractmethod
    def parse_response(self, response: requests.Response) -> pd.DataFrame:
        """Parses the response object and returns a DataFrame
        Args:
            response (requests.Response) Response object
        """

    @abstractmethod
    def add_response(self, response: pd.DataFrame) -> None:
        """Adds an HTTP response to the database.

        Args:
            response (pd.DataFrame): Response data in DataFrame format.
        """

    @abstractmethod
    def register(self, registry: Registry) -> None:
        """Registers the project

        registry (Registry): Dataclass containing metadata about the current project.
        """

    @abstractmethod
    def project_exists(self, *args, **kwargs) -> bool:
        """Checks existence of a scraping project"""

    @abstractmethod
    def request_exists(self, *args, **kwargs) -> bool:
        """Checks existence of a scraping request"""

    @abstractmethod
    def summary(self) -> dict:
        """Summarizes the results of the current scrape project."""


# ------------------------------------------------------------------------------------------------ #
class Repo(ABC):
    """Abstract base class for app data, review repositories."""

    @abstractmethod
    def get(self, tablename: str, *args, **kwargs) -> pd.DataFrame:
        """Queries the database and returns a result in DataFrame format."""

    @abstractmethod
    def add(self, data: pd.DataFrame, tablename: str) -> None:
        """Adds a DataFrame to the Database

        Args:
            data (pd.DataFrame): The data
            tablename (str): Name of table into which the data will be added.
        """

    @abstractmethod
    def update(self, data: pd.DataFrame, tablename: str) -> None:
        """Updates the table with the existing data.  This is essentially a replace operation

        Args:
            data (pd.DataFrame): The data to replace existing data
            tablename (str): The table name.

        """

    @abstractmethod
    def remove(self, *args, **kwargs) -> None:
        """Removes rows from the database"""
