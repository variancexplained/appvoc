#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/data/repo/uow.py                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 12:55:21 am                                                #
# Modified   : Thursday August 10th 2023 11:32:39 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

from appvoc.infrastructure.database.base import Database
from appvoc.data.repo.base import Repo


# ------------------------------------------------------------------------------------------------ #
#                                       UNIT OF WORK CLASS                                         #
# ------------------------------------------------------------------------------------------------ #
class UoW:
    """Unit of Work class encapsulating the repositories used in project objects.

    Args:
        database (Database): A Database instance from the dependency injector container.
        content (Repo): The content repository
        task (Repo): The task repository

    """

    def __init__(
        self,
        database: Database,
        appdata_repo: Repo,
        rating_repo: Repo,
        review_repo: Repo,
        appdata_project_repo: Repo,
        job_repo: Repo,
        rating_jobrun_repo: Repo,
        review_jobrun_repo: Repo,
        review_request_repo: Repo,
    ) -> None:
        self._database = database
        self._appdata_repo = appdata_repo
        self._review_repo = review_repo
        self._rating_repo = rating_repo
        self._appdata_project_repo = appdata_project_repo
        self._job_repo = job_repo
        self._rating_jobrun_repo = rating_jobrun_repo
        self._review_jobrun_repo = review_jobrun_repo
        self._review_request_repo = review_request_repo

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def database(self) -> Database:
        return self._database

    @property
    def appdata_repo(self) -> Repo:
        return self._appdata_repo(database=self._database)

    @property
    def review_repo(self) -> Repo:
        return self._review_repo(database=self._database)

    @property
    def rating_repo(self) -> Repo:
        return self._rating_repo(database=self._database)

    @property
    def appdata_project_repo(self) -> Repo:
        return self._appdata_project_repo(database=self._database)

    @property
    def job_repo(self) -> Repo:
        return self._job_repo(database=self._database)

    @property
    def rating_jobrun_repo(self) -> Repo:
        return self._rating_jobrun_repo(database=self._database)

    @property
    def review_jobrun_repo(self) -> Repo:
        return self._review_jobrun_repo(database=self._database)

    @property
    def review_request_repo(self) -> Repo:
        return self._review_request_repo(database=self._database)

    def connect(self) -> None:
        """Connects the database"""
        self._database.connect()

    def begin(self) -> None:
        """Begin a transaction"""
        self._database.begin()

    def save(self) -> None:
        """Saves changes to the underlying sqlite context"""
        self._database.commit()

    def rollback(self) -> None:
        """Returns state of sqlite to the point of the last commit."""
        self._database.rollback()

    def close(self) -> None:
        """Closes the sqlite connection."""
        self._database.close()
