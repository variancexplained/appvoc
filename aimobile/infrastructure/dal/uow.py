#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/infrastructure/dal/uow.py                                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 5th 2023 04:11:43 am                                                #
# Modified   : Friday April 21st 2023 09:31:13 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""DataCentre Module Encapsulates all repositories used in this appstore scraping service."""
from aimobile.infrastructure.dal.base import UoW
from aimobile.infrastructure.dal.repo import Repo
from aimobile.infrastructure.dal.base import Database


# ------------------------------------------------------------------------------------------------ #
class AppStoreUoW(UoW):
    """Appstore Unit of Work

    This Unit of Work class has the sole responsibility of ensuring that all appstore repositories
    share the same database context.
    Args:
        appdata_repository (type[Repo]): A Repo class type
        review_repository (type[Repo]): A Repo class type
        database (Database): A Database instance from the dependency injector container.

    """

    def __init__(
        self,
        database: Database,
        appdata_repository: type[Repo] = Repo,
        review_repository: type[Repo] = Repo,
    ) -> None:
        self._database = database
        self._appdata_repository = appdata_repository
        self._review_repository = review_repository

    @property
    def database(self) -> Database:
        return self._database

    @property
    def appdata_repository(self) -> Repo:
        """Returns a appdata repository instantiated with the sqlite context."""
        return self._appdata_repository(database=self._database)

    @property
    def review_repository(self) -> Repo:
        """Returns a project repository instantiated with the sqlite context."""
        return self._review_repository(database=self._database)

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
