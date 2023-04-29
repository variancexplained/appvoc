#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Task    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/repo/task.py                                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday April 28th 2023 01:48:48 pm                                                  #
# Modified   : Friday April 28th 2023 10:58:49 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Task Repository Module"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import logging

import pandas as pd

from aimobile.data.base import Task
from aimobile.data.repo.base import Repo
from aimobile.infrastructure.dal.base import Database




# ------------------------------------------------------------------------------------------------ #
class TaskRepo(Repo):
    """Task Repository

    Args:
        database(Database): Database containing data to access.
    """

    __name = "project"

    def __init__(self, database: Database) -> None:
        super().__init__(name=self.__name, database=database)
        self._logger = logging.getLogger(f"{self.__class__.__naProject

    @property
    def summary(self) -> pd.DataFrame:
        return self.getall()

    def get(self, id: str) -> Task:
        """Returns a Task instance for the designated id

        Args:
            id (str): The project identifier.
        """
        df = super().get(id=id)
        return Task.from_df(df=df)

    def add(self, data: Task) -> None:
        """Adds a project to the repository.

        Args:
            data (Task): Adds a project to the repository.
        """
        data = data.to_df()
        self._database.insert(data=data, tablename=self._name, if_exists="append")
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def replace(self, data: Task) -> None:  # pragma: no cover
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        data = data.to_df()
        self._database.insert(data=data, tablename=self._name, if_exists="replace")
        msg = f"Replace {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)

    def update(self, data: Task) -> None:
        """Updates the project in the repo.

        Args:
            data (Task): Task instance.

        """
        query = f"UPDATE {self._name} SET project.state = :state, project.pages = :pages, project.updated = :updated, project.ended = :ended WHERE id =:id"
        params = {
            "state": data.state,
            "pages": data.pages,
            "updated": data.updated,
            "ended": data.ended,
            "id": data.id,
        }
        self._database.update(query=query, params=params)
