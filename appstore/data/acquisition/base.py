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
# Modified   : Sunday July 30th 2023 06:41:54 am                                                   #
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

# ------------------------------------------------------------------------------------------------ #


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
    def update_job(self, result: Result) -> None:
        """Updates the job run's statistics."""

    @abstractmethod
    def end_job(self) -> None:
        """Ends a job run"""


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Result(ABC):
    """Interface for result objects which encapsulate HTTP responses."""

    response: Any  # Can be a list of responses (async) or a single response.
    success: Any  # Can be a count or a boolean

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
    started: datetime
    updated: datetime
    ended: datetime
    runs: int
    elapsed: int
    status: str

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

    def end(self) -> None:
        now = datetime.now()
        self.updated = now
        self.ended = now
        self.elapsed += (self.ended - self.started).total_seconds()
        self.status = "completed"
        msg = f"\nJob Completed:\n{self.__str__}"
        self._logger.info(msg)

    @abstractclassmethod
    def from_df(cls, df: pd.DataFrame) -> Job:
        """Creates a job from a Dataframe object."""
        df = df.iloc[0]
        return cls(
            id=df["id"],  # noqa
            controller=df["controller"],
            category_id=df["category_id"],
            category=df["category"],
            started=df["started"],
            updated=df["updated"],
            ended=df["ended"],
            runs=df["runs"],
            elapsed=df["elapsed"],
            status=df["status"],
        )
