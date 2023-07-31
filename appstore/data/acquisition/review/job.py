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
# Modified   : Sunday July 30th 2023 07:53:33 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass

import pandas as pd

from appstore.data.acquisition.review.result import ReviewResult
from appstore.data.acquisition.base import Job


# ------------------------------------------------------------------------------------------------ #
@dataclass
class ReviewJob(Job):
    """Review Job object

    Inherits the following from the base class:
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
    """

    apps: int = None
    apps_per_second: float = None
    reviews: int = None
    reviews_per_second: float = None
    total_requests: int = None
    successful_requests: int = None
    failed_requests: int = None

    def update(self, result: ReviewResult) -> None:
        """Adds result metadata"""
        super().update(result=result)
        self.apps += result.success
        self.apps_per_second = round(self.apps / self.run_elapsed, 2)
        self.reviews += result.reviews
        self.reviews_per_second = round(self.reviews / self.run_elapsed, 2)
        self.total_requests += result.requests
        self.successful_requests += result.successes
        self.failed_requests += result.fails

    def announce(self) -> None:
        """Writes progress to the log"""
        self._logger.info(self.__str__)

    @classmethod
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
            job_elapsed=df["job_elapsed"],
            run_elapsed=df["run_elapsed"],
            apps=df["apps"],
            apps_per_second=df["apps_per_second"],
            reviews=df["reviews"],
            reviews_per_second=df["reviews_per_second"],
            total_requests=df["total_requests"],
            successful_requests=df["successful_requests"],
            failed_requests=df["failed_requests"],
            status=df["status"],
        )
