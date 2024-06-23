#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/data/acquisition/rating/job.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday July 30th 2023 02:36:49 am                                                   #
# Modified   : Wednesday August 9th 2023 10:40:06 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from appvoc.data.acquisition.rating.result import RatingResult
from appvoc.data.acquisition.base import Job, JobRun


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RatingJobRun(JobRun):
    """Rating Job object

    Inherits the following from the base class:
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
    """

    apps: int = 0
    apps_per_second: float = 0
    bytes_per_second: float = 0
    size_ave: float = 0

    def add_result(self, result: RatingResult) -> None:
        """Adds Iterate through responses to update metrics. Result will have a list of response objects."""
        super().add_result(result=result)
        self.apps += result.apps
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

    @classmethod
    def from_df(cls, df: pd.DataFrame, existing: bool = False) -> RatingJobRun:
        """Creates a jobrun from a Dataframe object.

        Args:
            df (pd.DataFrame): DataFrame containing jobrun data
            existing (bool): Whether to recreate the existing jobrun, or create new.

        """
        df = df.iloc[0]
        if isinstance(df["completed"], str):
            df["completed"] = datetime.strptime(df["completed"], "%m/%d/%Y %H:%M:%S")
        if existing:
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
                bytes_per_second=df["bytes_per_second"],
                complete=df["complete"],
                completed=df["completed"],
            )
        else:
            return cls(
                jobid=df["jobid"],
                controller=df["controller"],
                category_id=df["category_id"],
                category=df["category"],
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
