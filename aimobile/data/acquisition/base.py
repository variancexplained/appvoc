#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/base.py                                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 06:49:10 pm                                                  #
# Modified   : Sunday April 30th 2023 08:23:16 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import requests

import pandas as pd


# ------------------------------------------------------------------------------------------------ #
class Controller(ABC):
    """Defines the Abstract Base Class for Controller subclasses

    Controllers are responsible for the data acquisition process, taking a list of terms
    or categories to process, they orchestrate the data acquisition through scraper objects,
    and directly manage persistence of the results, as well as Project and Task objects.
    """

    @abstractmethod
    def scrape(self, *args, **kwargs) -> None:
        """Entry point for scraping operations."""

    @abstractmethod
    def _start_project(self) -> None:
        """Creates and persists a Project object"""

    @abstractmethod
    def _update_project(self) -> None:
        """Updates the project"""

    @abstractmethod
    def _complete_project(self) -> None:
        """Sets project status to 'complete'"""

    @abstractmethod
    def _create_task(self) -> None:
        """Creates a Task object and persists it to the repository."""


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Result:
    scraper: type[Scraper]  # The class type of the Scraper
    host: str  # The base url from which the data were obtained.
    page: int  # The result page
    pages: int  # The number of pages cumulatively processed up to this result
    size: int  # Size of result in bytes
    results: int  # The number of records returned
    content: pd.DataFrame  # The content of the response.


# ------------------------------------------------------------------------------------------------ #
class Scraper(ABC):
    """Defines the Scraper interface for app scraper objects returning app data in batch pages"""

    @abstractmethod
    def __iter__(self) -> Scraper:
        """Returns a RequestGenerator object"""

    @abstractmethod
    def __next__(self) -> Result:
        """Generates the next Request object and returns a Result object."""

    @abstractmethod
    def _is_valid_response(self, response: requests.Response) -> bool:
        """Evaluates the response and returns its validity."""

    @abstractmethod
    def _parse_response(self, response: requests.Response) -> Result:
        """Parses the response and returns a Result object."""
