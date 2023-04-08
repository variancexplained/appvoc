#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Opportunity Discovery in Mobile Applications                             #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/data/scraper/appstore/dal/datacentre.py                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 5th 2023 04:11:43 am                                                #
# Modified   : Thursday April 6th 2023 02:17:27 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""DataCentre Module Encapsulates all repositories used in this appstore scraping service."""
from aimobile.data.scraper.appstore.dal.appdata import AppStoreDataRepo
from aimobile.data.scraper.appstore.database.sqlite import SQLiteDatabase
from aimobile.data.scraper.appstore.dal.project import AppStoreProjectRepo


# ------------------------------------------------------------------------------------------------ #
class DataCentre:
    """DataCentre implements the Unit of Work Pattern

    The repositories are instantiated with a common database context, controlled by the
    DataCentre class.

    Args:
        database (Database): The underlying database instance.


    """

    def __init__(
        self,
        database: SQLiteDatabase,
        appdata_repository: AppStoreDataRepo,
        project_repository=AppStoreProjectRepo,
    ) -> None:
        self._database = database
        self._appdata_repository = appdata_repository
        self._project_repository = project_repository

    @property
    def database(self) -> SQLiteDatabase:
        return self._database

    @property
    def appdata_repository(self) -> AppStoreDataRepo:
        """Returns a appdata repository instantiated with the database context."""
        return self._appdata_repository(database=self._database)

    @property
    def project_repository(self) -> AppStoreProjectRepo:
        """Returns a project repository instantiated with the database context."""
        return self._project_repository(database=self._database)

    def begin(self) -> None:
        """Begin a transaction"""
        self._database.begin()

    def save(self) -> None:
        """Saves changes to the underlying database context"""
        self._database.commit()

    def rollback(self) -> None:
        """Returns state of database to the point of the last commit."""
        self._database.rollback()

    def close(self) -> None:
        """Closes the database connection."""
        self._database.close()

    def dispose(self) -> None:
        """Disposes of the database and releases the resources."""
        self._database.dispose()
