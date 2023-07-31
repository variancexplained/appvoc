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
# Modified   : Sunday July 30th 2023 10:14:41 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging
from abc import abstractmethod
from typing import Union

import pandas as pd
import numpy as np
from appstore.data.acquisition.base import Job
from appstore.data.acquisition.review.job import ReviewJob
from appstore.data.acquisition.rating.job import RatingJob
from appstore.data.storage.base import Repo
from appstore.infrastructure.database.base import Database
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME, INTEGER, BIGINT, FLOAT


# ------------------------------------------------------------------------------------------------ #
class JobRepo(Repo):
    """Repository tracking progress of ETL

    Args:
        database(Database): Database containing data to access.
    """

    def __init__(self, name: str, database: Database) -> None:
        super().__init__(name=name, database=database)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @abstractmethod
    def add(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """

    @abstractmethod
    def get(self, id: str, dtypes: dict = None, parse_dates: dict = None) -> Job:  # noqa
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
        """

    @abstractmethod
    def next(self) -> Job:
        """Returns a randomly selected job not yet completed"""

    @abstractmethod
    def getall(self, dtypes: dict = None, parse_dates: dict = None) -> pd.DataFrame:
        """Returns all data in the repository."""
        return super().getall(dtypes=dtypes, parse_dates=parse_dates)

    @abstractmethod
    def update(self, job: Job) -> None:
        """Updates a job in the database"""

    @abstractmethod
    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """

    @property
    def summary(self) -> pd.DataFrame:
        """Summarizes the app data by category"""
        df = self.getall()
        df = df.groupby(["controller", "status"])["id"].count().reset_index()
        df.columns = ["Controller", "Status", "Jobs"]
        return df


# ------------------------------------------------------------------------------------------------ #
#                                 RATING DATAFRAME DATA TYPES                                      #
# ------------------------------------------------------------------------------------------------ #
RATING_JOB_DATAFRAME_DTYPES = {
    "id": "string",
    "controller": "category",
    "category_id": "category",
    "category": "category",
    "runs": np.int64,
    "job_elapsed": np.int64,
    "run_elapsed": np.int64,
    "status": "string",
    "apps": np.int64,
    "apps_per_second": np.float64,
    "total_requests": np.int64,
    "successful_requests": np.int64,
    "failed_requests": np.int64,
}
RATING_JOB_PARSE_DATES = {
    "started": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
    "updated": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
    "ended": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
}
# ------------------------------------------------------------------------------------------------ #
#                                  RATING DATABASE DATA TYPES                                      #
# ------------------------------------------------------------------------------------------------ #
RATING_JOB_DATABASE_DTYPES = {
    "id": VARCHAR(32),
    "controller": VARCHAR(64),
    "category_id": VARCHAR(8),
    "category": VARCHAR(64),
    "runs": INTEGER,
    "started": DATETIME,
    "updated": DATETIME,
    "ended": DATETIME,
    "job_elapsed": BIGINT,
    "run_elapsed": BIGINT,
    "status": VARCHAR(16),
    "apps": BIGINT,
    "apps_per_second": FLOAT,
    "total_requests": BIGINT,
    "successful_requests": BIGINT,
    "failed_requests": BIGINT,
}


# ------------------------------------------------------------------------------------------------ #
class RatingJobRepo(JobRepo):
    __name = "rating_job"

    def __init__(self, database: Database) -> None:
        super().__init__(self.__name, database)

    def add(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data,
            tablename=self._name,
            dtype=RATING_JOB_DATABASE_DTYPES,
            if_exists="append",
        )
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def get(
        self,
        id: Union[str, int],
        dtypes: dict = RATING_JOB_DATAFRAME_DTYPES,
        parse_dates: dict = RATING_JOB_PARSE_DATES,
    ) -> Job:
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
        """
        query = f"SELECT * FROM {self._name} WHERE id = :id;"
        params = {"id": id}
        job = self._database.query(
            query=query, params=params, dtypes=dtypes, parse_dates=parse_dates
        )
        return RatingJob.from_df(df=job)

    def next(self) -> Job:
        """Returns a randomly selected job not yet completed"""

        df = self.getall()
        # First get any in-progress jobs
        jobs = df.loc[df["status"] == "in_progress"]
        if len(jobs) == 0:
            # Get jobs not started
            jobs = df.loc[df["status"] == "not_started"]

        try:
            job = jobs.sample(n=1)

        except Exception:
            msg = "All jobs complete."
            self._logger.info(msg)
            return None
        else:
            return RatingJob.from_df(job)

    def getall(
        self,
        dtypes: dict = RATING_JOB_DATAFRAME_DTYPES,
        parse_dates: dict = RATING_JOB_PARSE_DATES,
    ) -> pd.DataFrame:
        """Returns all data in the repository."""
        return super().getall(dtypes=dtypes, parse_dates=parse_dates)

    def update(self, job: Job) -> None:
        """Updates a job in the database"""
        query = f"""UPDATE {self._name} SET
        controller = :controller,
        category_id = :category_id,
        category = :category,
        started = :started,
        updated = :updated,
        ended = :ended,
        runs = :runs,
        job_elapsed = :job_elapsed,
        run_elapsed = :run_elapsed,
        status = :status,
        apps = :apps,
        apps_per_second = :apps_per_second,
        total_requests = :total_requests,
        successful_requests = :successful_requests,
        failed_requests =:failed_requests
        WHERE id = :id;"""
        params = {
            "controller": job.controller,
            "category_id": job.category_id,
            "category": job.category,
            "started": job.started,
            "updated": job.updated,
            "ended": job.ended,
            "runs": job.runs,
            "job_elapsed": job.job_elapsed,
            "run_elapsed": job.run_elapsed,
            "status": job.status,
            "apps": job.apps,
            "apps_per_second": job.apps_per_second,
            "total_requests": job.total_requests,
            "successful_requests": job.successful_requests,
            "failed_requests": job.failed_requests,
            "id": job.id,
        }
        self._database.update(query=query, params=params)

    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data, tablename=self._name, dtype=RATING_JOB_DATABASE_DTYPES, if_exists="replace"
        )
        msg = f"Replace {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)


# ------------------------------------------------------------------------------------------------ #
#                                REVIEW DATAFRAME DATA TYPES                                       #
# ------------------------------------------------------------------------------------------------ #
REVIEW_JOB_DATAFRAME_DTYPES = {
    "id": "string",
    "controller": "category",
    "category_id": "category",
    "category": "category",
    "runs": np.int64,
    "job_elapsed": np.int64,
    "run_elapsed": np.int64,
    "status": "string",
    "apps": np.int64,
    "apps_per_second": np.float64,
    "reviews": np.int64,
    "reviews_per_second": np.float64,
    "total_requests": np.int64,
    "successful_requests": np.int64,
    "failed_requests": np.int64,
}
REVIEW_JOB_PARSE_DATES = {
    "started": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
    "updated": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
    "ended": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
}
# ------------------------------------------------------------------------------------------------ #
#                                      DATABASE DATA TYPES                                         #
# ------------------------------------------------------------------------------------------------ #
REVIEW_JOB_DATABASE_DTYPES = {
    "id": VARCHAR(32),
    "controller": VARCHAR(64),
    "category_id": VARCHAR(8),
    "category": VARCHAR(64),
    "runs": INTEGER,
    "started": DATETIME,
    "updated": DATETIME,
    "ended": DATETIME,
    "job_elapsed": BIGINT,
    "run_elapsed": BIGINT,
    "status": VARCHAR(16),
    "apps": BIGINT,
    "apps_per_second": FLOAT,
    "reviews": BIGINT,
    "reviews_per_second": FLOAT,
    "total_requests": BIGINT,
    "successful_requests": BIGINT,
    "failed_requests": BIGINT,
}


# ------------------------------------------------------------------------------------------------ #
class ReviewJobRepo(JobRepo):
    __name = "review_job"

    def __init__(self, database: Database) -> None:
        super().__init__(self.__name, database)

    def add(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data,
            tablename=self._name,
            dtype=REVIEW_JOB_DATABASE_DTYPES,
            if_exists="append",
        )
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def get(
        self,
        id: Union[str, int],
        dtypes: dict = REVIEW_JOB_DATAFRAME_DTYPES,
        parse_dates: dict = REVIEW_JOB_PARSE_DATES,
    ) -> Job:
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
        """
        query = f"SELECT * FROM {self._name} WHERE id = :id;"
        params = {"id": id}
        job = self._database.query(
            query=query, params=params, dtypes=dtypes, parse_dates=parse_dates
        )
        return ReviewJob.from_df(df=job)

    def next(self) -> Job:
        """Returns a randomly selected job not yet completed"""

        df = self.getall()
        # First get any in-progress jobs
        jobs = df.loc[df["status"] == "in_progress"]
        if len(jobs) == 0:
            # Get jobs not started
            jobs = df.loc[df["status"] == "not_started"]

        try:
            job = jobs.sample(n=1)

        except Exception:
            msg = "All jobs complete."
            self._logger.info(msg)
            return None
        else:
            return ReviewJob.from_df(job)

    def getall(
        self,
        dtypes: dict = REVIEW_JOB_DATAFRAME_DTYPES,
        parse_dates: dict = REVIEW_JOB_PARSE_DATES,
    ) -> pd.DataFrame:
        """Returns all data in the repository."""
        return super().getall(dtypes=dtypes, parse_dates=parse_dates)

    def update(self, job: Job) -> None:
        """Updates a job in the database"""
        query = f"""UPDATE {self._name} SET
        controller = :controller,
        category_id = :category_id,
        category = :category,
        started = :started,
        updated = :updated,
        ended = :ended,
        runs = :runs,
        job_elapsed = :job_elapsed,
        run_elapsed = :run_elapsed,
        status = :status,
        apps = :apps,
        apps_per_second = :apps_per_second,
        reviews = :reviews,
        reviews_per_second = :reviews_per_second,
        total_requests = :total_requests,
        successful_requests = :successful_requests,
        failed_requests =:failed_requests
        WHERE id = :id;"""
        params = {
            "controller": job.controller,
            "category_id": job.category_id,
            "category": job.category,
            "started": job.started,
            "updated": job.updated,
            "ended": job.ended,
            "runs": job.runs,
            "job_elapsed": job.job_elapsed,
            "run_elapsed": job.run_elapsed,
            "status": job.status,
            "apps": job.apps,
            "apps_per_second": job.apps_per_second,
            "reviews": job.reviews,
            "reviews_per_second": job.reviews_per_second,
            "total_requests": job.total_requests,
            "successful_requests": job.successful_requests,
            "failed_requests": job.failed_requests,
            "id": job.id,
        }
        self._database.update(query=query, params=params)

    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data, tablename=self._name, dtype=REVIEW_JOB_DATABASE_DTYPES, if_exists="replace"
        )
        msg = f"Replace {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)
