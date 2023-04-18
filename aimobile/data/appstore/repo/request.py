#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Request    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/appstore/repo/request.py                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 06:11:59 am                                                  #
# Modified   : Tuesday April 18th 2023 11:02:40 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

from itertools import count
import pandas as pd

from aimobile.data.base import Repo
from aimobile.framework.database.sqlite import SQLiteDatabase
from aimobile.data.appstore.entity.request import AppStoreRequest
from aimobile.framework.exception import exceptions


# ------------------------------------------------------------------------------------------------ #
class AppStoreRequestRepo(Repo):
    """Repository of scraping requests.

    Args:
        database (SQLiteDatabase): Appstore Database
    """

    __id_gen = count(1)

    def __init__(self, database: SQLiteDatabase) -> None:
        self._database = database
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def get(self, id: int) -> AppStoreRequest:
        """Retrieves a request by id.

        Args:
            id (int): Request id

        Raises: ObjectNotFound if the request was not found.
        """
        query = "SELECT * FROM request WHERE request.id = :id;"
        params = {"id": id}

        df = self._database.query(query=query, params=params)
        if df.shape[0] == 0:
            raise exceptions.ObjectNotFound(id=id)
        return AppStoreRequest.from_df(df.loc[0])

    def get_by_name(self, name: str, as_df=None) -> AppStoreRequest:
        """Retrieves a request by name.

        Args:
            name (str): Request id

        Raises: ObjectNotFound if the request was not found.
        """
        query = "SELECT * FROM request WHERE request.name = :name;"
        params = {"name": name}

        df = self._database.query(query=query, params=params)
        if df.shape[0] == 0:
            raise exceptions.ObjectNotFound(name=name)
        if as_df is True:
            return df
        else:
            return AppStoreRequest.from_df(df.loc[0])

    def getall(self) -> pd.DataFrame:
        """Returns a DataFrame of all requests in the repository

        raises ObjectNotFound if the repository is empty.
        """
        query = "SELECT * FROM request;"
        df = self._database.query(query=query)
        if df.shape[0] == 0:
            raise exceptions.ObjectNotFound()
        return df

    def add(self, request: dict) -> None:
        """Adds a request entity to the repository

        Args:
            data (AppStoreRequest): A Request object.

        """
        request.id = next(AppStoreRequestRepo.__id_gen)
        df = request.as_df()
        self._database.insert(data=df, tablename="request")

    def update(self, request: AppStoreRequest) -> None:  # pragma: no cover
        """Updates a request in the repo

        Args:
            request (AppStoreRequest): Request data

        """
        raise NotImplementedError()

    def remove(self, id: int) -> None:  # pragma: no cover
        """Removes a request from the repo.

        Args:
            id (int): Request identifier.
        """
        raise NotImplementedError()

    def drop(self) -> None:
        """Drops the request table."""
        query = "DROP TABLE IF EXISTS request;"
        self._database.execute(query=query)