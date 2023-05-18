#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/repo/project.py                                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday April 28th 2023 01:48:48 pm                                                  #
# Modified   : Sunday May 7th 2023 07:18:11 am                                                     #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Project Repository Module"""
from __future__ import annotations
import logging
from typing import Union

import pandas as pd

from aimobile.data.acquisition.project import Project
from aimobile.data.repo.base import Repo
from aimobile.infrastructure.dal.base import Database


# ------------------------------------------------------------------------------------------------ #
class ProjectRepo(Repo):
    """Project Repository

    Args:
        database(Database): Database containing data to access.
    """

    __name = "project"

    def __init__(self, database: Database) -> None:
        super().__init__(name=self.__name, database=database)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def summary(self) -> pd.DataFrame:
        return self.getall()

    def get(self, id: str) -> Project:
        """Returns a Project instance for the designated id

        Args:
            id (str): The project identifier.
        """
        df = super().get(id=id)
        return Project.from_df(df=df)

    def get_project(self, controller: str, term: str) -> Union[Project, None]:
        """Obtain the project matching the parameters.

        Args:
            controller (str): The class name for the controller
            term (str): The search term

        """
        query = f"SELECT * FROM {self._name} WHERE controller = :controller AND term = :term;"
        params = {"controller": controller, "term": term}
        result = self._database.query(query=query, params=params)
        if len(result) == 0:
            return None
        else:
            return Project.from_df(result)

    def add(self, data: Project) -> None:
        """Adds a project to the repository.

        Args:
            data (Project): Adds a project to the repository.
        """
        data = data.as_df()
        self._database.insert(data=data, tablename=self._name, if_exists="append")
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def replace(self, data: Project) -> None:  # pragma: no cover
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        data = data.as_df()
        self._database.insert(data=data, tablename=self._name, if_exists="replace")
        msg = f"Replace {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)

    def update(self, data: Project) -> None:
        """Updates the project in the repo.

        Args:
            data (Project): Project instance.

        """
        query = f"UPDATE {self._name} SET {self._name}.status = :status, {self._name}.pages = :pages, {self._name}.vpages = :vpages, {self._name}.apps = :apps, {self._name}.updated = :updated, {self._name}.completed = :completed WHERE {self._name}.id = :id;"
        params = {
            "controller": data.controller,
            "term": data.term,
            "status": data.status,
            "pages": data.pages,
            "vpages": data.vpages,
            "apps": data.apps,
            "started": data.started,
            "updated": data.updated,
            "completed": data.completed,
            "id": data.id,
        }
        self._database.update(query=query, params=params)


# ------------------------------------------------------------------------------------------------ #
class RatingProjectRepo(Repo):
    """Rating Project Repository

    Args:
        database(Database): Database containing data to access.
    """

    __name = "rating_project"

    def __init__(self, database: Database) -> None:
        super().__init__(name=self.__name, database=database)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def summary(self) -> pd.DataFrame:
        projects = self.getall()
        summary = projects["category"].value_counts().reset_index()
        summary.columns = ["Category", "Apps"]
        return summary

    def get(self, id: str) -> Project:
        """Returns a Project instance for the designated id

        Args:
            id (str): The project identifier.
        """
        return super().get(id=id)

    def add(self, data: pd.DataFrame) -> None:
        """Adds a project to the repository.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(data=data, tablename=self._name, if_exists="append")
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def replace(self, data: Project) -> None:  # pragma: no cover
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(data=data, tablename=self._name, if_exists="replace")
        msg = f"Replace {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)

    def update(self, data: Project) -> None:
        """Updates the project in the repo.

        Args:
            data (Project): Project instance.

        """
        msg = f"No update method for the {self.__class__.__name} respository."
        raise NotImplementedError(msg)
