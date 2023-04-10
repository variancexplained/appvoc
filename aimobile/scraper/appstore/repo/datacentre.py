#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/scraper/appstore/repo/datacentre.py                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 5th 2023 04:11:43 am                                                #
# Modified   : Monday April 10th 2023 10:54:02 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""DataCentre Module Encapsulates all repositories used in this appstore scraping service."""
from aimobile.scraper.appstore.repo.appdata import AppStoreDataRepo
from aimobile.scraper.appstore.database.sqlite import SQLiteDatabase
from aimobile.scraper.appstore.repo.project import AppStoreProjectRepo
from aimobile.scraper.appstore.repo.request import AppStoreRequestRepo
from aimobile.scraper.appstore.repo.review import AppStoreReviewRepo


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
        appdata_repository: type[AppStoreDataRepo] = AppStoreDataRepo,
        project_repository: type[AppStoreProjectRepo] = AppStoreProjectRepo,
        request_repository: type[AppStoreRequestRepo] = AppStoreRequestRepo,
        review_repository: type[AppStoreReviewRepo] = AppStoreReviewRepo,
    ) -> None:
        self._database = database.connect()
        self._appdata_repository = appdata_repository
        self._project_repository = project_repository
        self._request_repository = request_repository
        self._review_repository = review_repository

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

    @property
    def request_repository(self) -> AppStoreRequestRepo:
        """Returns a project repository instantiated with the database context."""
        return self._request_repository(database=self._database)

    @property
    def review_repository(self) -> AppStoreReviewRepo:
        """Returns a project repository instantiated with the database context."""
        return self._review_repository(database=self._database)

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
