#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/infrastructure/dal/uow.py                                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 5th 2023 04:11:43 am                                                #
# Modified   : Thursday April 20th 2023 04:09:56 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""DataCentre Module Encapsulates all repositories used in this appstore scraping service."""
from aimobile.data.x_appstore.repo.appdata import AppStoreDataRepo
from aimobile.infrastructure.dal.sqlite import SQLiteDatabase
from aimobile.infrastructure.dal.mysql import MySQLDatabase
from aimobile.data.x_appstore.repo.review import AppStoreReviewRepo
from aimobile.data.x_appstore.repo.rating import AppStoreRatingsRepo


# ------------------------------------------------------------------------------------------------ #
class UnitofWork:
    """Unit of Work

    The repositories are instantiated with a common sqlite context, controlled by the
    DataCentre class.

    Args:
        sqlite (Database): The underlying sqlite instance.

    """

    def __init__(
        self,
        sqlite: SQLiteDatabase,
        mysql: MySQLDatabase,
        appdata_repository: type[AppDataRepo] = AppDataRepo,
        review_repository: type[AppStoreReviewRepo] = AppStoreReviewRepo,
        rating_repository: type[AppStoreRatingsRepo] = AppStoreRatingsRepo,
    ) -> None:
        self._sqlite = sqlite.connect()
        self._mysql = mysql.connect()
        self._appdata_repository = appdata_repository
        self._review_repository = review_repository
        self._rating_repository = rating_repository

    @property
    def appdata_repository(self) -> AppStoreDataRepo:
        """Returns a appdata repository instantiated with the sqlite context."""
        return self._appdata_repository(database=self._sqlite)

    @property
    def rating_repository(self) -> AppStoreRatingsRepo:
        """Returns a appdata repository instantiated with the sqlite context."""
        return self._rating_repository(database=self._sqlite)

    @property
    def review_repository(self) -> AppStoreReviewRepo:
        """Returns a project repository instantiated with the sqlite context."""
        return self._review_repository(database=self._mysql)

    def begin(self) -> None:
        """Begin a transaction"""
        self._sqlite.begin()
        self._mysql.begin()

    def save(self) -> None:
        """Saves changes to the underlying sqlite context"""
        self._sqlite.commit()
        self._mysql.commit()

    def rollback(self) -> None:
        """Returns state of sqlite to the point of the last commit."""
        self._sqlite.rollback()
        self._mysql.rollback()

    def close(self) -> None:
        """Closes the sqlite connection."""
        self._sqlite.close()
        self._mysql.close()

    def dispose(self) -> None:
        """Disposes of the sqlite and releases the resources."""
        self._sqlite.dispose()
        self._mysql.dispose()
