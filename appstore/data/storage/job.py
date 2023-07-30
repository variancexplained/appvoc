#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /appstore/data/storage/job.py                                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday July 29th 2023 02:06:11 pm                                                 #
# Modified   : Sunday July 30th 2023 06:27:22 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

import pandas as pd

from appstore.data.acquisition.job import Job
from appstore.data.storage.base import Repo
from appstore.infrastructure.database.base import Database
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME, INTEGER

# ------------------------------------------------------------------------------------------------ #
#                                    DATAFRAME DATA TYPES                                          #
# ------------------------------------------------------------------------------------------------ #
DATAFRAME_DTYPES = {
    "id": "string",
    "controller": "category",
    "category_id": "category",
    "category": "category",
    "runs": "int64",
    "elapsed": "int64",
    "status": "string",
}
PARSE_DATES = {
    "started": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
    "updated": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
    "ended": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
}
# ------------------------------------------------------------------------------------------------ #
#                                      DATABASE DATA TYPES                                         #
# ------------------------------------------------------------------------------------------------ #
DATABASE_DTYPES = {
    "id": VARCHAR(32),
    "controller": VARCHAR(64),
    "category_id": VARCHAR(8),
    "category": VARCHAR(64),
    "runs": INTEGER,
    "started": DATETIME,
    "ended": DATETIME,
    "elapsed": INTEGER,
    "status": VARCHAR(16),
}


# ------------------------------------------------------------------------------------------------ #
class JobRepo(Repo):
    """Repository tracking progress of ETL

    Args:
        database(Database): Database containing data to access.
    """

    def __init__(self, name: str, database: Database) -> None:
        super().__init__(name=name, database=database)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def add(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data,
            tablename=self._name,
            dtype=DATABASE_DTYPES,
            if_exists="append",
        )
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def get(
        self, id: str, dtypes: dict = DATAFRAME_DTYPES, parse_dates: dict = None  # noqa
    ) -> Job:
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
            dtypes (dict): Dictionary mapping of column to data types
            parse_dates (dict): Dictionary of columns and keyword arguments for datetime parsing.
        """
        job = super().get(id=id, dtypes=dtypes, parse_dates=parse_dates)
        return Job.from_df(df=job)

    def get_next(self, controller: str) -> Job:
        """Returns a randomly selected job not yet completed.

        Args:
            controller (str): The controller executing the job
        """
        df = self.getall()
        # First get any in-progress jobs
        jobs = df.loc[df["status"] == "in_progress"]
        if len(jobs) == 0:
            # Get jobs not started
            jobs = df.loc[df["status"] == "not_started"]

        try:
            job = jobs.sample(n=1)

        except Exception:
            msg = f"All jobs complete for {controller}."
            self._logger.info(msg)
            return None
        else:
            return Job.from_df(job)

    def get_by_controller(self, controller: str, status: str = None) -> pd.DataFrame:
        """Returns the jobs for the given controller

        Args:
            controller (str): A job controller
            status (bool): Status of job, either 'not_started', 'in_progress', or 'completed'.
        """
        df = self.getall()
        jobs = df.loc[df["controller"] == controller]
        if status is not None:
            jobs = jobs[jobs["status"] == status]
        if len(jobs) == 0:
            msg = f"No jobs found for {controller}"
            self._logger.exception(msg)
            raise KeyError(msg)
        return jobs

    def getall(self) -> pd.DataFrame:
        """Returns all data in the repository."""

        return super().getall(dtypes=DATAFRAME_DTYPES, parse_dates=PARSE_DATES)

    def update(self, job: Job) -> None:
        """Updates a job in the database"""
        query = f"UPDATE {self._name} SET controller = :controller, category_id = :category_id, category = :category, started = :started, ended = :ended, status = :status WHERE id = :id;"
        params = {
            "controller": job.controller,
            "category_id": job.category_id,
            "category": job.category,
            "started": job.started,
            "updated": job.updated,
            "ended": job.ended,
            "runs": job.runs,
            "status": job.status,
            "id": job.id,
        }
        self._database.update(query=query, params=params)

    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data, tablename=self._name, dtype=DATABASE_DTYPES, if_exists="replace"
        )
        msg = f"Replace {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)

    @property
    def summary(self) -> pd.DataFrame:
        """Summarizes the app data by category"""
        df = self.getall()
        df = df.groupby(["controller", "status"])["id"].count().reset_index()
        df.columns = ["Controller", "Status", "Jobs"]
        return df


# ------------------------------------------------------------------------------------------------ #
class RatingJobRepo(JobRepo):
    __name = "rating_job"

    def __init__(self, database: Database) -> None:
        super().__init__(self.__name, database)


# ------------------------------------------------------------------------------------------------ #
class ReviewJobRepo(JobRepo):
    __name = "review_job"

    def __init__(self, database: Database) -> None:
        super().__init__(self.__name, database)
