#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/repo/uow.py                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 12:55:21 am                                                #
# Modified   : Saturday April 29th 2023 06:02:38 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

from aimobile.infrastructure.dal.base import Database
from aimobile.data.repo.base import Repo


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

    def __init__(self, database: Database, project_repo: Repo, task_repo: Repo) -> None:
        self._database = database
        self._source_repo = None
        self._target_repo = None
        self._project_repo = project_repo
        self._task_repo = task_repo
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def database(self) -> Database:
        return self._database

    @property
    def project_repo(self) -> Repo:
        return self._project_repo

    @property
    def task_repo(self) -> Repo:
        return self._task_repo

    @property
    def source_repo(self) -> Repo:
        return self._source_repo

    @source_repo.setter
    def source_repo(self, source_repo: Repo) -> None:
        self._source_repo = source_repo

    @property
    def target_repo(self) -> Repo:
        return self._target_repo

    @target_repo.setter
    def target_repo(self, target_repo: Repo) -> None:
        self._target_repo = target_repo

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
