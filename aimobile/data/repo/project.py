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
# Modified   : Saturday May 20th 2023 01:25:51 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Project Repository Module"""
from __future__ import annotations
import logging
from typing import Union

import pandas as pd

from aimobile.data.acquisition.appdata.project import AppDataProject
from aimobile.data.repo.base import Repo
from aimobile.infrastructure.dal.base import Database


# ------------------------------------------------------------------------------------------------ #
class AppDataProjectRepo(Repo):
    """Project Repository

    Args:
        database(Database): Database containing data to access.
    """

    __name = "appdata_project"

    def __init__(self, database: Database) -> None:
        super().__init__(name=self.__name, database=database)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def summary(self) -> pd.DataFrame:
        return self.getall()

    def get(self, id: str) -> AppDataProject:
        """Returns a Project instance for the designated id

        Args:
            id (str): The project identifier.
        """
        df = super().get(id=id)
        return AppDataProject.from_df(df=df)

    def get_project(self, controller: str, term: str) -> Union[AppDataProject, None]:
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
        elif len(result) == 1:
            return AppDataProject.from_df(result)
        else:
            msg = f"Exception. Multiple projects for {term}."
            self._logger.error(msg)
            raise Exception(msg)

    def add(self, data: AppDataProject) -> None:
        """Adds a project to the repository.

        Args:
            data (Project): Adds a project to the repository.
        """
        data = data.as_df()
        self._database.insert(data=data, tablename=self._name, if_exists="append")
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def replace(self, data: AppDataProject) -> None:  # pragma: no cover
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        data = data.as_df()
        self._database.insert(data=data, tablename=self._name, if_exists="replace")
        msg = f"Replace {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)

    def update(self, data: AppDataProject) -> None:
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

    def exists(self, controller: str, term: str) -> bool:
        """Assesses the existence of an entity in the database.

        Args:
            id (Union[str,int]): The app id.
        """
        query = f"SELECT EXISTS(SELECT 1 FROM {self._name} WHERE controller = :controller AND term = :term);"
        params = {"controller": controller, "term": term}
        return self._database.exists(query=query, params=params)
