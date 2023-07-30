#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/acquisition/rating/job.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday July 30th 2023 02:36:49 am                                                   #
# Modified   : Sunday July 30th 2023 06:33:47 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
from datetime import datetime

from appstore.data.acquisition.rating.result import RatingResult
from appstore.data.acquisition.job import Job, JobRun


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RatingJob(Job):
    """Rating Job object"""


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RatingJobRun(JobRun):
    """Monitors progress of the RatingController.

    Inherits the following from the base class:
        job: Job
        started: datetime
        ended: datetime
        duration: str
    """

    apps: int = None
    apps_per_second: float = None
    total_requests: int = None
    successful_requests: int = None
    failed_requests: int = None

    def update_job_run(self, result: RatingResult) -> None:
        """Adds result metadata"""
        now = datetime.now()
        self.elapsed = (now - self.started).total_seconds()
        self.apps += result.success
        self.apps_per_second = round(self.apps / self.elapsed, 2)
        self.total_requests += result.total
        self.successful_requests += result.success
        self.failed_requests += result.fail

    def end_job_run(self) -> None:
        """Sets end datetime and duration."""
        self.ended = datetime.now()
        self.elapsed = (self.ended - self.started).total_seconds()

    def announce_job_run(self) -> None:
        """Writes progress to the log"""
        self._logger.info(self.__str__)
