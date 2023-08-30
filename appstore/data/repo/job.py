#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /appstore/data/repo/job.py                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday July 29th 2023 02:06:11 pm                                                 #
# Modified   : Tuesday August 29th 2023 05:54:34 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging
from typing import Union

import pandas as pd
import numpy as np
from appstore.data.acquisition.base import Job
from appstore.data.acquisition.review.job import ReviewJobRun
from appstore.data.acquisition.rating.job import RatingJobRun
from appstore.data.repo.base import Repo
from appstore.infrastructure.database.base import Database
from appstore.infrastructure.file.config import FileConfig
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME, BIGINT, FLOAT, TINYINT

# ------------------------------------------------------------------------------------------------ #
#                                 RATING DATAFRAME DATA TYPES                                      #
# ------------------------------------------------------------------------------------------------ #
JOB_DATAFRAME_DTYPES = {
    "id": "string",
    "controller": "category",
    "category_id": "category",
    "category": "category",
    "complete": bool,
}
JOB_PARSE_DATES = {
    "completed": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
}

JOB_DATABASE_DTYPES = {
    "id": VARCHAR(32),
    "controller": VARCHAR(64),
    "category_id": VARCHAR(8),
    "category": VARCHAR(64),
    "complete": TINYINT,
    "completed": VARCHAR(64),
}


class JobRepo(Repo):
    """Repository tracking progress of ETL

    Args:
        database(Database): Database containing data to access.
    """

    __name = "job"

    def __init__(self, database: Database, config=FileConfig) -> None:
        super().__init__(name=self.__name, database=database, config=config)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def add(self, job: Job) -> None:
        """Adds a job to the repo.

        Args:
            job (Job): A Job object.
        """
        try:
            if self.exists(id=job.id):
                msg = f"Job {job.id} already exists."
                self._logger.exception(msg)
                raise ValueError(msg)  # noqa
        except Exception:
            pass  # noqa

        df = job.as_df()
        self.load(data=df)

    def load(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        data = self._parse_datetime(data=data, dtcols="completed")

        self._database.insert(
            data=data, tablename=self._name, dtype=JOB_DATABASE_DTYPES, if_exists="append"
        )

        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def get(
        self, id: str, dtypes: dict = JOB_DATAFRAME_DTYPES, parse_dates: dict = JOB_PARSE_DATES
    ) -> Job:  # noqa
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
        """
        df = super().get(id=id, dtypes=dtypes, parse_dates=parse_dates)
        return Job.from_df(df=df)

    def next(self, controller: str) -> Job:
        """Returns a randomly selected job not yet completed"""

        df = self.getall()
        jobs = df.loc[(df["complete"] == False) & (df["controller"] == controller)]  # noqa
        if len(jobs) == 0:
            return None
        else:
            job = jobs.sample(n=1)
            return Job.from_df(df=job)

    def getall(
        self, dtypes: dict = JOB_DATAFRAME_DTYPES, parse_dates: dict = JOB_PARSE_DATES
    ) -> pd.DataFrame:
        """Returns all data in the repository."""
        return super().getall(dtypes=dtypes, parse_dates=parse_dates)

    def update(self, job: Job) -> None:
        """Updates a job in the database"""
        query = (
            f"UPDATE {self._name} SET complete = :complete, completed = :completed WHERE id = :id;"
        )
        params = {
            "complete": job.complete,
            "completed": job.completed,
            "id": job.id,
        }
        self._database.update(query=query, params=params)

    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        data = self._parse_datetime(data=data, dtcols="completed")

        self._database.insert(
            data=data, tablename=self._name, dtype=JOB_DATABASE_DTYPES, if_exists="replace"
        )
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    @property
    def summary(self) -> pd.DataFrame:
        """Summarizes the app data by category"""
        return self.getall()


# ------------------------------------------------------------------------------------------------ #
#                           RATING JOBRUN DATAFRAME DATA TYPES                                     #
# ------------------------------------------------------------------------------------------------ #
RATING_JOBRUN_DATAFRAME_DTYPES = {
    "id": "string",
    "jobid": "string",
    "controller": "string",
    "category_id": "string",
    "category": "string",
    "elapsed": np.int64,
    "client_errors": np.int64,
    "server_errors": np.int64,
    "data_errors": np.int64,
    "errors": np.int64,
    "size": np.int64,
    "size_ave": np.float64,
    "apps": np.int64,
    "apps_per_second": np.float64,
    "bytes_per_second": np.float64,
    "complete": bool,
}
RATING_JOBRUN_PARSE_DATES = {
    "completed": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
    "started": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
    "ended": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
}
# ------------------------------------------------------------------------------------------------ #
#                                  RATING DATABASE DATA TYPES                                      #
# ------------------------------------------------------------------------------------------------ #
RATING_JOBRUN_DATABASE_DTYPES = {
    "id": VARCHAR(64),
    "jobid": VARCHAR(32),
    "controller": VARCHAR(64),
    "category_id": VARCHAR(8),
    "category": VARCHAR(64),
    "started": DATETIME,
    "ended": DATETIME,
    "elapsed": BIGINT,
    "client_errors": BIGINT,
    "server_errors": BIGINT,
    "data_errors": BIGINT,
    "errors": BIGINT,
    "size": BIGINT,
    "size_ave": FLOAT,
    "apps": BIGINT,
    "apps_per_second": FLOAT,
    "bytes_per_second": FLOAT,
    "completed": DATETIME,
    "complete": TINYINT,
}


# ------------------------------------------------------------------------------------------------ #
class RatingJobRunRepo(Repo):
    __name = "rating_jobrun"

    def __init__(self, database: Database, config=FileConfig) -> None:
        super().__init__(name=self.__name, database=database, config=config)

    def add(self, jobrun: RatingJobRun) -> None:
        """Adds a job to the repo.

        Args:
            jobrun (RatingJobRun): A rating job run object.
        """
        try:
            if self.exists(id=jobrun.id):
                msg = f"Job run {jobrun.id} already exists."
                self._logger.exception(msg)
                raise ValueError(msg)  # noqa
        except Exception:
            pass  # noqa

        df = jobrun.as_df()
        self.load(data=df)

    def load(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        data = self._parse_datetime(data=data, dtcols=["started", "ended", "completed"])

        self._database.insert(
            data=data,
            tablename=self._name,
            dtype=RATING_JOBRUN_DATABASE_DTYPES,
            if_exists="append",
        )
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def get(
        self,
        id: Union[str, int],
        dtypes: dict = RATING_JOBRUN_DATAFRAME_DTYPES,
        parse_dates: dict = RATING_JOBRUN_PARSE_DATES,
    ) -> RatingJobRun:
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
        """
        query = f"SELECT * FROM {self._name} WHERE id = :id;"
        params = {"id": id}
        jobrun = self._database.query(
            query=query, params=params, dtypes=dtypes, parse_dates=parse_dates
        )
        try:
            return RatingJobRun.from_df(df=jobrun)
        except Exception as e:
            msg = f"Exception of type {type(e)} occurred.\n{e}"
            self._logger.debug(msg)
            return None

    def getall(
        self,
        dtypes: dict = RATING_JOBRUN_DATAFRAME_DTYPES,
        parse_dates: dict = RATING_JOBRUN_PARSE_DATES,
    ) -> pd.DataFrame:
        """Returns all data in the repository."""
        return super().getall(dtypes=dtypes, parse_dates=parse_dates)

    def update(self, jobrun: RatingJobRun) -> None:
        """Updates a job in the database"""
        query = f"""UPDATE {self._name} SET
            started =:started,
            ended =:ended,
            elapsed =:elapsed,
            client_errors =:client_errors,
            server_errors =:server_errors,
            data_errors =:data_errors,
            errors =:errors,
            size =:size,
            size_ave =:size_ave,
            apps =:apps,
            apps_per_second =:apps_per_second,
            bytes_per_second =:bytes_per_second,
            complete = :complete,
            completed =:completed
            WHERE id = :id;"""
        params = {
            "started": jobrun.started,
            "ended": jobrun.ended,
            "elapsed": jobrun.elapsed,
            "client_errors": jobrun.client_errors,
            "server_errors": jobrun.server_errors,
            "data_errors": jobrun.data_errors,
            "errors": jobrun.errors,
            "size": jobrun.size,
            "size_ave": jobrun.size_ave,
            "apps": jobrun.apps,
            "apps_per_second": jobrun.apps_per_second,
            "bytes_per_second": jobrun.bytes_per_second,
            "complete": jobrun.complete,
            "completed": jobrun.completed,
            "id": jobrun.id,
        }
        self._database.update(query=query, params=params)

    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        data = self._parse_datetime(data=data, dtcols=["started", "ended", "completed"])
        self._database.insert(
            data=data,
            tablename=self._name,
            dtype=RATING_JOBRUN_DATABASE_DTYPES,
            if_exists="replace",
        )
        msg = f"Replace {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)


# ------------------------------------------------------------------------------------------------ #
#                           REVIEW JOBRUN DATAFRAME DATA TYPES                                     #
# ------------------------------------------------------------------------------------------------ #
REVIEW_JOBRUN_DATAFRAME_DTYPES = {
    "id": "string",
    "jobid": "string",
    "controller": "string",
    "category_id": "string",
    "category": "string",
    "elapsed": np.int64,
    "client_errors": np.int64,
    "server_errors": np.int64,
    "data_errors": np.int64,
    "errors": np.int64,
    "size": np.int64,
    "size_ave": np.float64,
    "apps": np.int64,
    "apps_per_second": np.float64,
    "bytes_per_second": np.float64,
    "reviews": np.int64,
    "reviews_per_second": np.float64,
    "complete": bool,
}
REVIEW_JOBRUN_PARSE_DATES = {
    "completed": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
    "started": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
    "ended": {"errors": "coerce", "format": "%Y-%m-%d %H:%M:%S", "exact": False},
}
# ------------------------------------------------------------------------------------------------ #
#                                  REVIEW DATABASE DATA TYPES                                      #
# ------------------------------------------------------------------------------------------------ #
REVIEW_JOBRUN_DATABASE_DTYPES = {
    "id": VARCHAR(64),
    "jobid": VARCHAR(32),
    "controller": VARCHAR(64),
    "category_id": VARCHAR(8),
    "category": VARCHAR(64),
    "started": DATETIME,
    "ended": DATETIME,
    "elapsed": BIGINT,
    "client_errors": BIGINT,
    "server_errors": BIGINT,
    "data_errors": BIGINT,
    "errors": BIGINT,
    "size": BIGINT,
    "size_ave": FLOAT,
    "apps": BIGINT,
    "apps_per_second": FLOAT,
    "bytes_per_second": FLOAT,
    "reviews": BIGINT,
    "reviews_per_second": FLOAT,
    "completed": VARCHAR(64),
    "complete": TINYINT,
}


# ------------------------------------------------------------------------------------------------ #
class ReviewJobRunRepo(Repo):
    __name = "review_jobrun"

    def __init__(self, database: Database, config=FileConfig) -> None:
        super().__init__(name=self.__name, database=database, config=config)

    def add(self, jobrun: ReviewJobRun) -> None:
        """Adds a job to the repo.

        Args:
            jobrun (ReviewJobRun): A review job run object.
        """
        try:
            if self.exists(id=jobrun.id):
                msg = f"Job run {jobrun.id} already exists."
                self._logger.exception(msg)
                raise ValueError(msg)  # noqa
        except Exception:
            pass  # noqa

        df = jobrun.as_df()

        self.load(data=df)

    def load(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        data = self._parse_datetime(data=data, dtcols=["started", "ended", "completed"])

        self._database.insert(
            data=data,
            tablename=self._name,
            dtype=REVIEW_JOBRUN_DATABASE_DTYPES,
            if_exists="append",
        )
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def get(
        self,
        id: Union[str, int],
        dtypes: dict = REVIEW_JOBRUN_DATAFRAME_DTYPES,
        parse_dates: dict = REVIEW_JOBRUN_PARSE_DATES,
    ) -> ReviewJobRun:
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
        """
        query = f"SELECT * FROM {self._name} WHERE id = :id;"
        params = {"id": id}
        jobrun = self._database.query(
            query=query, params=params, dtypes=dtypes, parse_dates=parse_dates
        )
        return ReviewJobRun.from_df(df=jobrun)

    def getall(
        self,
        dtypes: dict = REVIEW_JOBRUN_DATAFRAME_DTYPES,
        parse_dates: dict = REVIEW_JOBRUN_PARSE_DATES,
    ) -> pd.DataFrame:
        """Returns all data in the repository."""
        return super().getall(dtypes=dtypes, parse_dates=parse_dates)

    def update(self, jobrun: ReviewJobRun) -> None:
        """Updates a job in the database"""
        query = f"""UPDATE {self._name} SET
            started =:started,
            ended =:ended,
            elapsed =:elapsed,
            client_errors =:client_errors,
            server_errors =:server_errors,
            data_errors =:data_errors,
            errors =:errors,
            size =:size,
            size_ave =:size_ave,
            apps =:apps,
            apps_per_second =:apps_per_second,
            bytes_per_second =:bytes_per_second,
            reviews =:reviews,
            reviews_per_second =:reviews_per_second,
            complete = :complete,
            completed =:completed
            WHERE id = :id;"""
        params = {
            "started": jobrun.started,
            "ended": jobrun.ended,
            "elapsed": jobrun.elapsed,
            "client_errors": jobrun.client_errors,
            "server_errors": jobrun.server_errors,
            "data_errors": jobrun.data_errors,
            "errors": jobrun.errors,
            "size": jobrun.size,
            "size_ave": jobrun.size_ave,
            "apps": jobrun.apps,
            "apps_per_second": jobrun.apps_per_second,
            "bytes_per_second": jobrun.bytes_per_second,
            "reviews": jobrun.reviews,
            "reviews_per_second": jobrun.reviews_per_second,
            "complete": jobrun.complete,
            "completed": jobrun.completed,
            "id": jobrun.id,
        }
        self._database.update(query=query, params=params)

    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        data = self._parse_datetime(data=data, dtcols=["started", "ended", "completed"])

        self._database.insert(
            data=data,
            tablename=self._name,
            dtype=REVIEW_JOBRUN_DATABASE_DTYPES,
            if_exists="replace",
        )
        msg = f"Replace {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)
