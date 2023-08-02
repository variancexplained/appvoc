#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/acquisition/review/job.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday July 30th 2023 02:36:49 am                                                   #
# Modified   : Wednesday August 2nd 2023 07:37:19 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass

import pandas as pd

from appstore.data.acquisition.review.result import ReviewResult
from appstore.data.acquisition.base import JobRun, Job


# ------------------------------------------------------------------------------------------------ #
@dataclass
class ReviewJobRun(JobRun):
    """Review Job object

    Inherits the following from the base class:
        id: str  # noqa
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
        size_ave: float = 0
        complete: bool = False
        completed: datetime = None
    """

    apps: int = 0
    apps_per_second: float = 0
    reviews: int = 0
    reviews_per_second: float = 0
    size_ave: float = 0

    def add_result(self, result: ReviewResult) -> None:
        """Adds Iterate through responses to update metrics. Result will have a list of response objects."""
        super().add_result(result=result)
        self.reviews += result.reviews
        self.apps_per_second = round(self.apps / self.elapsed, 2)
        self.reviews_per_second = round(self.reviews / self.elapsed, 2)
        self.size_ave = self.size / self.apps
        super().end()

    def announce(self) -> None:
        """Writes progress to the log"""
        self._logger.info(self.__str__())

    @classmethod
    def from_job(cls, job: Job) -> JobRun:  # noqa
        """Creates a JobRun from a Job object."""
        return cls(
            jobid=job.id,
            controller=job.controller,
            category_id=job.category_id,
            category=job.category,
        )

    @classmethod
    def from_jobrun(cls, jobrun: JobRun) -> JobRun:  # noqa
        """Creates a JobRun from a JobRun object."""
        return cls(
            jobid=jobrun.jobid,
            controller=jobrun.controller,
            category_id=jobrun.category_id,
            category=jobrun.category,
        )

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> ReviewJobRun:
        """Creates a job from a Dataframe object."""
        df = df.iloc[0]
        return cls(
            id=df["id"],  # noqa
            jobid=df["jobid"],
            controller=df["controller"],
            category_id=df["category_id"],
            category=df["category"],
            started=df["started"],
            ended=df["ended"],
            elapsed=df["elapsed"],
            client_errors=df["client_errors"],
            server_errors=df["server_errors"],
            data_errors=df["data_errors"],
            errors=df["errors"],
            size=df["size"],
            size_ave=df["size_ave"],
            apps=df["apps"],
            apps_per_second=df["apps_per_second"],
            reviews=df["reviews"],
            reviews_per_second=df["reviews_per_second"],
            complete=df["complete"],
            completed=df["completed"],
        )
