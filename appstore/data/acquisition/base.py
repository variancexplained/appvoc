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
# Modified   : Wednesday August 2nd 2023 09:27:44 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
import os
from uuid import uuid4
import logging
from datetime import datetime
from dotenv import load_dotenv
from abc import ABC, abstractmethod, abstractclassmethod
from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from appstore.base import DTO
from appstore.data.storage.base import Repo


# ------------------------------------------------------------------------------------------------ #
class Director(ABC):
    """Iterator serving jobs to the controller."""

    def __init__(self, jobrun_repo: Repo, job_repo: Repo) -> None:
        self._jobrun_repo = jobrun_repo
        self._job_repo = job_repo
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
    def persist(self, result: Result) -> None:
        """Starts a job run"""

    @abstractmethod
    def update_jobrun(self, jobrun: JobRun, result: Result) -> None:
        """Updates teh jobrun with the result"""

    @abstractmethod
    def end_jobrun(self, jobrun: JobRun) -> None:
        """Ends a job run"""


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
    id: str = None
    controller: str = None
    category_id: str = None
    category: str = None
    complete: bool = False
    completed: datetime = None

    def __post_init__(self) -> None:
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> Job:
        df = df.iloc[0].T
        logging.debug(df)
        return cls(
            id=df["id"],
            controller=df["controller"],
            category_id=df["category_id"],
            category=df["category"],
            complete=df["complete"],
            completed=datetime.strftime(df["completed"], "%Y-%m-%d %H:%M:%S"),
        )

    def end(self) -> None:
        self.completed = datetime.now()
        self.complete = True
        msg = f"\nJob Completed.{self.__str__()}"
        self._logger.info(msg)


# ------------------------------------------------------------------------------------------------ #
@dataclass
class JobRun(DTO):
    """Encapsulates a job run entity"""

    id: str = None
    jobid: str = None
    controller: str = None
    category_id: str = None
    category: str = None
    started: datetime = None
    ended: datetime = None
    elapsed: int = 0
    client_errors: int = 0
    server_errors: int = 0
    data_errors: int = 0
    errors: int = 0
    size: int = 0
    complete: bool = False
    completed: datetime = None

    def __post_init__(self) -> None:
        self.id = uuid4()
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def start(self) -> None:
        self.started = datetime.now()
        self.complete = False
        msg = f"\nJobRun for job {self.jobid} Started"
        self._logger.info(msg)

    @abstractmethod
    def add_result(self, result: Result) -> None:
        """Updates the JobRun statistics."""
        now = datetime.now()
        self.ended = now
        self.elapsed = (now - self.started).total_seconds()
        self.client_errors += result.client_errors
        self.server_errors += result.server_errors
        self.data_errors += result.data_errors
        self.errors += self.client_errors + self.server_errors + self.data_errors
        self.size += result.size
        self.status = "in_progress"

    def end(self) -> None:
        self.complete = True
        self.completed = datetime.now()
        msg = f"\nJobRun Completed.{self.__str__()}"
        self._logger.info(msg)

    def announce(self) -> None:
        """Writes progress to the log"""
        msg = self.__str__()
        self._logger.info(msg)

    @abstractclassmethod
    def from_job(cls, job: Job) -> JobRun:  # noqa
        """Creates a JobRun from a Job object."""

    @abstractclassmethod
    def from_jobrun(cls, jobrun: JobRun) -> JobRun:  # noqa
        """Creates a JobRun from a JobRun object."""

    @abstractclassmethod
    def from_df(cls, df: pd.DataFrame) -> JobRun:  # noqa
        """Creates a JobRun from a DataFrame."""


# ------------------------------------------------------------------------------------------------ #
@dataclass(frozen=True)
class ErrorCodes:
    no_response: int = 602
    response_type_error: int = 605
    data_error: int = 610


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Validator(ABC):
    """Validates response"""

    response: Any = None
    valid: bool = True
    status_code: int = None
    error_code: int = None
    msg: str = None
    client_error: bool = False
    server_error: bool = False

    @abstractmethod
    def is_valid(self, response: Any) -> bool:
        """Validates the response object"""


# ------------------------------------------------------------------------------------------------ #
@dataclass
class App(DTO):
    id: str
    name: str
    category_id: str
    category: str


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Result(DTO):
    content: list[dict] = field(default_factory=list)
    size: int = 0
    errors: int = 0

    def __post_init__(self) -> None:
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @abstractmethod
    def add_response(self, response: Any, *args, **kwargs) -> None:
        """Adds result content to the instance"""

    def get_result(self) -> pd.DataFrame:
        """Returns the result in DataFrame format"""
        return pd.DataFrame(self.content)

    def is_valid(self) -> bool:
        return len(self.content) > self.errors
