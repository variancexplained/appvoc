#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/acquisition/base.py                                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 06:49:10 pm                                                  #
# Modified   : Sunday July 30th 2023 07:56:27 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from abc import ABC, abstractmethod, abstractclassmethod
from dataclasses import dataclass
from typing import Any

import pandas as pd

from appstore.base import DTO
from appstore.data.storage.base import Repo


# ------------------------------------------------------------------------------------------------ #
class Director(ABC):
    """Iterator serving jobs to the controller."""

    def __init__(self, repo: Repo) -> None:
        self._repo = repo
        self._job = None

    @property
    def job(self) -> Job:
        return self._job

    @abstractmethod
    def __iter__(self) -> None:
        """Initializes the job iterator"""

    @abstractmethod
    def __next__(self) -> Director:
        """Sets the next job and returns an instance of this iterator"""


# ------------------------------------------------------------------------------------------------ #
class Controller(ABC):
    """Defines the Abstract Base Class for Controller subclasses

    Controllers are responsible for the data acquisition process, taking a list of terms
    or categories to process, they orchestrate the data acquisition through scraper objects,
    and directly manage persistence of the results, as well as Project and Task objects.
    """

    def is_locked(self, *args, **kwargs) -> None:
        """Entry point for scraping operations."""
        load_dotenv()
        return os.getenv(self.__class__.__name__, False) in (True, "true", "True")

    @abstractmethod
    def start_job(self, job: Job) -> None:
        """Starts a job run"""

    @abstractmethod
    def end_job(self, job: Job) -> None:
        """Ends a job run"""

    @abstractmethod
    def save_results(self, result: Result) -> None:
        """Saves results to Database"""


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Response(DTO):
    """Encapsulates a parsed response from a Scraper object."""

    status: bool = True

    @abstractclassmethod
    def create(cls, *args, **kwargs) -> Response:  # noqa
        """Factory method that creates a parsed response object"""


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Result(ABC):
    """Interface for result objects which encapsulate HTTP responses."""

    response: Any
    # Can be a list of responses (async) or a single response.
    requests: int = 0
    # The number of requests in the result. For synchronous requests,
    # this will be 1.
    successes: int = 0
    # The number of successful requests in the result.
    fails: int = 0
    # The number of failed requests in the result

    @abstractmethod
    def update_result(self, response: Any = None) -> None:
        """Updates the response object as well as metadata associated with subclasses

        Args:
           response (Any): The parsed HTTP response.
        """

    @abstractmethod
    def is_valid(self) -> bool:
        """Returns the validity of the result as a boolean."""

    @abstractmethod
    def as_df(self) -> bool:
        """Returns the response as a dataframe."""


# ------------------------------------------------------------------------------------------------ #
class Scraper(ABC):
    """Defines the Scraper interface for app scraper objects returning app data in batch pages"""

    @abstractmethod
    def __iter__(self) -> Scraper:
        """Returns a RequestGenerator object"""

    @abstractmethod
    def __next__(self) -> Result:
        """Generates and submits the next request and returns a Result object."""


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Project(DTO):
    """Project"""

    @abstractclassmethod
    def from_df(cls, df: pd.DataFrame) -> Project:  # noqa
        """Takes a DataFrame and creates a Project object."""


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Job(DTO):
    """Encapsulates a job entity"""

    id: str  # noqa
    controller: str
    category_id: str
    category: str
    started: datetime = None
    updated: datetime = None
    ended: datetime = None
    runs: int = None
    job_elapsed: int = None
    run_elapsed: int = None
    status: str = None

    def __post_init__(self) -> None:
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def start(self) -> None:
        now = datetime.now()
        self.runs += 1
        if self.status == "not_started":
            self.status = "in_progress"
            self.started = now
            self.updated = now
            msg = f"\nJob Started:\n{self.__str__}"
        else:
            self.updated = now
            msg = f"\nJob Restarted:\n{self.__str__}"

        self._logger.info(msg)

    @abstractmethod
    def update(self, result: Result) -> None:
        """Updates the job's statistics."""
        now = datetime.now()
        elapsed = (now - self.started).total_seconds()
        self.updated = now
        self.job_elapsed += elapsed
        self.run_elapsed = elapsed
        self.total_requests += result.requests
        self.successful_requests += result.success
        self.failed_requests += result.failed

    def end(self) -> None:
        now = datetime.now()
        elapsed = (self.ended - self.started).total_seconds()
        self.updated = now
        self.ended = now
        self.job_elapsed += elapsed
        self.run_elapsed = elapsed
        self.status = "completed"
        msg = f"\nJob Completed:\n{self.__str__}"
        self._logger.info(msg)

    @abstractclassmethod
    def from_df(cls, df: pd.DataFrame) -> Job:  # noqa
        """Creates a job from a Dataframe object."""

    @abstractmethod
    def announce(self) -> None:
        """Writes progress to the log"""
