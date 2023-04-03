#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/scraper/appstore/dal/project.py                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 06:11:59 am                                                  #
# Modified   : Sunday April 2nd 2023 10:56:16 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

import pandas as pd

from aimobile.data.scraper.appstore.dal.base import Repo
from aimobile.data.scraper.appstore.database.sqlite import SQLiteDatabase


# ------------------------------------------------------------------------------------------------ #
class ProjectRepo(Repo):
    """Repository of scraping projects.

    Args:
        database (SQLiteDatabase): Appstore Database
    """

    def __init__(self, database: SQLiteDatabase) -> None:
        self._database = database
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def get(self, id: str = None) -> pd.DataFrame:
        """Retrieves a project by id or all projects if id is None

        Args:
            id (str): Project id. Optional. If None, all projects are returned.
        """
        if id is not None:
            query = "SELECT * FROM project WHERE project.id = :id;"
            params = {"id": id}
        else:
            query = "SELECT * FROM project;"
            params = {}

        return self._database.query(query=query, params=params)

    def add(self, data: pd.DataFrame) -> None:
        """Adds a project to the database

        Args:
            data (pd.DataFrame): Project data in pandas DataFrame format.
        """
        self._database.insert(data=data, tablename="project")

    def update(self, data: dict) -> None:
        """Updates a project in the database.

        Args:
            data (dict): The data to replace existing data

        """
        project_data = data.to_dict(orient="records")
        query = "UPDATE projects SET end_page = ?, results = ?, state = ?, started = ?, ended = ?, duration = ? WHERE project_id = ?;"
        params = (
            project_data["end_page"],
            project_data["results"],
            project_data["state"],
            project_data["started"],
            project_data["ended"],
            project_data["duration"],
            project_data["project_id"],
        )
        self._database.update(query=query, params=params)

    def remove(self, category_name: str = None, project_id: str = None) -> None:
        """Removes rows from the database

        Args:
            category_name (str): Category from AppStoreCategories. Optional.
            project_id (str): Identifier for a scrape project. Optional.
        """
        if category_name is not None and project_id is not None:
            query = "DELETE FROM projects WHERE category_name = ? AND project_id = ?;"
            params = (
                category_name,
                project_id,
            )
        elif category_name is not None:
            query = "DELETE FROM projects WHERE category_name = ?;"
            params = (category_name,)
        elif project_id is not None:
            query = "DELETE FROM projects WHERE project_id = ?;"
            params = (project_id,)
        else:
            msg = "Remove method missing parameters."
            self._logger.error(msg)
            raise ValueError(msg)

        self._database.delete(query=query, params=params)
