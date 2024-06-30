#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/domain/app/job.py                                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday July 30th 2023 02:36:49 am                                                   #
# Modified   : Sunday June 30th 2024 12:22:30 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations

from dataclasses import dataclass

from appvoc.domain.job import Job, JobRun
from appvoc.domain.rating.response import RatingResponse


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RatingJobRun(JobRun):
    """Rating JobRun object

    Inherits the following from the base class:
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
    """

    apps: int = 0
    apps_per_second: float = 0
    bytes_per_second: float = 0
    size_ave: float = 0

    def add_response(self, response: RatingResponse) -> None:
        """Adds Iterate through responses to update metrics. Response will have a list of response objects."""
        super().add_response(response=response)
        self.apps += response.apps
        self.apps_per_second = round(self.apps / self.elapsed, 2)
        self.size_ave = self.size / self.apps
        self.bytes_per_second = round(self.size / self.elapsed, 2)

    @classmethod
    def from_job(cls, job: Job) -> JobRun:  # noqa
        """Creates a JobRun from a Job object."""
        return cls(
            jobid=job.id,
            controller=job.controller,
            category_id=job.category_id,
            category=job.category,
            started=None,
            ended=None,
            elapsed=0,
            client_errors=0,
            server_errors=0,
            data_errors=0,
            errors=0,
            size=0,
            size_ave=0,
            apps=0,
            apps_per_second=0,
            bytes_per_second=0,
            complete=False,
            completed=None,
        )
