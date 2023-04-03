#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/data/scraper/base.py                                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 3rd 2023 12:36:15 am                                                   #
# Modified   : Monday April 3rd 2023 05:36:19 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Base class for the Scraper service."""
from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod

import requests
import pandas as pd


# ------------------------------------------------------------------------------------------------ #
IMMUTABLE_TYPES: tuple = (str, int, float, bool, type(None))
SEQUENCE_TYPES: tuple = (list, tuple)


# ------------------------------------------------------------------------------------------------ #
#                                       ENTITY                                                     #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class Entity(ABC):
    """Defines the abstract base class for appdata and review entities."""

    @abstractmethod
    def from_result(self, result: dict, project: AbstractScraperProject) -> None:
        """Builds the entity from a request result

        Args:
            result (dict): Results from HTTP request
            project (AbstractScraperProject): The project definition
        """

    def as_dict(self) -> dict:
        """Returns a dictionary representation of the the Entity object."""
        return {k: v for k, v in self.__dict__.items()}


# ------------------------------------------------------------------------------------------------ #
#                                         REQUEST                                                  #
# ------------------------------------------------------------------------------------------------ #


@dataclass
class AbstractRequest(ABC):
    """Abstract class encapsulating the parameters of an HTTP request."""

    @property
    @abstractmethod
    def url(self) -> str:
        """Returns the base url for the HTTP request"""

    @property
    @abstractmethod
    def params(self) -> dict:
        """Dictionary containing parameters to be passed to the request method"""

    @property
    @abstractmethod
    def headers(self) -> dict:
        """Dictionary containing HTTP request header information."""

    @property
    @abstractmethod
    def timeout(self) -> int:
        """The number of seconds to wait for a response"""

    @property
    @abstractmethod
    def retries(self) -> int:
        """The maximum number of retry attempts should an exception be encountered."""


# ------------------------------------------------------------------------------------------------ #
#                                  ABSTRACT SCRAPER PROJECT                                        #
# ------------------------------------------------------------------------------------------------ #
class AbstractScraperProject(ABC):
    """Defines the base class for scraper projects."""


# ------------------------------------------------------------------------------------------------ #
#                              ABSTRACT APPDATA SCRAPER PROJECT                                    #
# ------------------------------------------------------------------------------------------------ #
class AbstractAppDataScraperProject(ABC):
    """Defines the base class for AppData scraper projects"""


# ------------------------------------------------------------------------------------------------ #
#                              ABSTRACT REVIEW SCRAPER PROJECT                                     #
# ------------------------------------------------------------------------------------------------ #
class AbstractReviewScraperProject(ABC):
    """Defines the base class for review scraper projects"""


# ------------------------------------------------------------------------------------------------ #
#                                  ABSTRACT SCRAPER FACTORY                                        #
# ------------------------------------------------------------------------------------------------ #
class AbstractScraperFactory(ABC):
    """Defines a factory interface with methods that return abstract appdata and review scrapers"""

    @abstractmethod
    def create_appdata_scraper(self, project: AbstractScraperProject) -> AbstractAppDataScraper:
        """Returns a concrete AppDataScraper

        Args:
            project (AbtractScraperProject): Object defining the projecturation for the scraper.
        """

    @abstractmethod
    def create_review_scraper(self, project: AbstractScraperProject) -> AbstractReviewScraper:
        """Returns a concrete ReviewScraper

        Args:
            project (AbtractScraperProject): Object defining the projecturation for the scraper.
        """


# ------------------------------------------------------------------------------------------------ #
#                                  ABSTRACT SCRAPER                                                #
# ------------------------------------------------------------------------------------------------ #
class AbstractScraper(ABC):
    """Defines the interface for app data scrapers"""

    def __init__(self, project: AbstractScraperProject) -> None:
        self._project = project

    @abstractmethod
    def scrape(self) -> None:
        """The entry point method that controls the scraping project"""

    @abstractmethod
    def summary(self) -> None:
        """Summarizes the scraping project."""

    @abstractmethod
    def _setup(self) -> None:
        """Creates, initializes and saves the project object"""

    @abstractmethod
    def _teardown(self) -> None:
        """Finalizes and stores the final project state."""

    @abstractmethod
    def _request(request_params: AbstractRequest) -> requests.Response:
        """Executes an HTTP request and returns a request Response object.

        Args:
            url (str): The base URL for the request
            headers (dict): Request header information
            params (dict): The dictionary of parameters passed two the request method
            timeout (int): The number of seconds to wait for a response, after which a ConnectionTimeout exception
                will be thrown.
            retries (int): The number of attempts to make if an exception is encountered.
        """

    @abstractmethod
    def _handle_exception(self, exception: Exception, attempt: int, retries: int) -> int:
        """Handles exceptions in the event of retries

        Args:
            exception (Exception): The exception encountered.
            attempt (int): The attempt count
            retries (int): The maximum number of retries

        Returns The next attempt number if attempts < retries
        Raises: Exception of attempts = retries.
        ."""

    @abstractmethod
    def _delay(self, delay: tuple, backoff_base: int = 2, attempt: int = 0) -> None:
        """Executes a delay of pseudo random duration using exponential backoff method as follows:

        t = r * b^a

        where:
        - t is the number of seconds delay
        - r is a random integer between a designated lower and upper bound
        - b is the backoff base of the exponential multiplier.
        - a is the attempt number.

        Args:
            delay (tuple): Contains lower and upper bound from which a random base delay is selected.
            backoff_base (int): The base of the exponential multiplier
            attempt (int): The retry attempt number
        """

    @abstractmethod
    def _parse_results(self, results: dict, entity: Entity) -> pd.DataFrame:
        """Iterates through results, extracts data of interest and returns a dataframe

        Args:
            results (dict): Dictionary containing the results extracted from the Response object.
            entity: (type[Entity]): Entity class that encapsulates the conversion from the
                result object.
        """

    @abstractmethod
    def add_data(self, data: pd.DataFrame) -> None:
        """Adds the data to the database

        Args:
            data (pd.DataFrame): Data to be persisted in the database.
        """

    @abstractmethod
    def add_project(self, project: AbstractScraperProject) -> None:
        """Adds the project to the project database.

        Args:
            project (AbstractScraperProject): Project definition
        """

    @abstractmethod
    def update_project(self, project: AbstractScraperProject) -> None:
        """Updates the project in the database with the current page and number of results.

        Args:
            project (AbstractScraperProject): Project definition
        """

    @abstractmethod
    def _set_next_request(self, request_params: AbstractRequest, results: dict) -> AbstractRequest:
        """Updates the request_params object for the next request

        Args:
            request_params (AbstractRequest): Encapsulates the parameters for the HTTP request.
            results (dict): The results from the prior request.
        """


# ------------------------------------------------------------------------------------------------ #
#                              ABSTRACT APPDATA SCRAPER                                            #
# ------------------------------------------------------------------------------------------------ #
class AbstractAppDataScraper(AbstractScraper):
    """Defines the interface for app data scrapers."""


# ------------------------------------------------------------------------------------------------ #
#                              ABSTRACT REVIEW SCRAPER                                             #
# ------------------------------------------------------------------------------------------------ #
class AbstractReviewScraper(AbstractScraper):
    """Defines the interface for review scrapers."""
