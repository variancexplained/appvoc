#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.14                                                                             #
# Filename   : /appvoc/domain/job.py                                                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday June 29th 2024 09:37:35 pm                                                 #
# Modified   : Saturday June 29th 2024 11:49:53 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
"""Job Module"""
from __future__ import annotations

import logging
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from appvoc.domain.entity import Entity
from appvoc.domain.response import Response


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Job(Entity):
    id: str = None
    controller: str = None
    category_id: str = None
    category: str = None
    complete: bool = False
    completed: datetime = None

    def __post_init__(self) -> None:
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @classmethod
    def from_dict(cls, job: dict) -> Job:
        """Instantiates a Job object from a dictionary."""

        return cls(
            id=job["id"],
            controller=job["controller"],
            category_id=job["category_id"],
            category=job["category"],
            complete=job["complete"],
            completed=datetime.strftime(job["completed"], "%Y-%m-%d %H:%M:%S"),
        )

    def end(self, completed: datetime) -> None:
        self.completed = completed
        self.complete = True


# ------------------------------------------------------------------------------------------------ #
@dataclass
class JobRun(Entity):
    """Encapsulates a job run entity"""

    id: str = None
    jobid: str = None
    controller: str = None
    category_id: str = None
    category: str = None
    started: datetime = None
    ended: datetime = None
    elapsed: int = 0
    size: int = 0
    complete: bool = False
    completed: datetime = None

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid4())
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def start(self) -> None:
        self.started = datetime.now()
        self.complete = False
        msg = f"\nJobRun for job {self.jobid} Started"
        self._logger.info(msg)

    def add_response(self, response: Response) -> None:
        """Updates the JobRun statistics."""
        now = datetime.now()
        self.ended = now
        self.elapsed = (now - self.started).total_seconds()
        self.errors += self.client_errors + self.server_errors + self.data_errors
        self.size += response.size

    def end(self) -> None:
        now = datetime.now()
        self.complete = True
        self.ended = now
        self.elapsed = (self.ended - self.started).total_seconds()
        self.completed = now

    def announce(self) -> None:
        """Writes progress to the log"""
        msg = self.__str__()
        self._logger.info(msg)

    @abstractmethod
    @classmethod
    def from_job(cls, job: Job) -> JobRun:  # noqa
        """Creates a JobRun from a Job object."""

    @abstractmethod
    @classmethod
    def from_dict(cls, jobrun: dict) -> JobRun:  # noqa
        """Creates a JobRun from a dictionary."""
