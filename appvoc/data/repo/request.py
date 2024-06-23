#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/data/repo/request.py                                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday August 9th 2023 04:55:46 pm                                               #
# Modified   : Tuesday August 29th 2023 05:40:53 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

import pandas as pd
import numpy as np

from appvoc.data.acquisition.review.request import ReviewRequest
from appvoc.data.repo.base import Repo
from appvoc.infrastructure.database.base import Database
from appvoc.infrastructure.file.config import FileConfig
from sqlalchemy.dialects.mysql import (
    VARCHAR,
    INTEGER,
)

# ------------------------------------------------------------------------------------------------ #
#                                    DATAFRAME DATA TYPES                                          #
# ------------------------------------------------------------------------------------------------ #
DATAFRAME_DTYPES = {
    "id": "string",
    "category_id": "category",
    "last_index": np.int64,
}

# ------------------------------------------------------------------------------------------------ #
#                                      DATABASE DATA TYPES                                         #
# ------------------------------------------------------------------------------------------------ #
DATABASE_DTYPES = {
    "id": VARCHAR(64),
    "category_id": VARCHAR(8),
    "last_index": INTEGER,
}


# ------------------------------------------------------------------------------------------------ #
class ReviewRequestRepo(Repo):
    """Repository for review requests

    Args:
        database(Database): Database containing data to access.
    """

    __name = "review_request"

    def __init__(self, database: Database, config=FileConfig) -> None:
        super().__init__(name=self.__name, database=database, config=config)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def add(self, request: ReviewRequest) -> None:
        """Adds a review request to the repository

        Args:
            request (ReviewRequest): Object containing details of the review HTTP request.
        """
        df = request.as_df()
        self.load(data=df)

    def load(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data, tablename=self._name, dtype=DATABASE_DTYPES, if_exists="append"
        )
        msg = f"Added {data.shape[0]} rows to the {self._name} repository."
        self._logger.debug(msg)

    def get(self, id: str, dtypes: dict = DATAFRAME_DTYPES, **kwargss) -> pd.DataFrame:
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
            dtypes (dict): Dictionary mapping of column to data types
            parse_dates (dict): Dictionary of columns and keyword arguments for datetime parsing.
        """
        df = super().get(id=id, dtypes=dtypes)
        if len(df) > 0:
            return ReviewRequest.from_df(df=df)
        else:
            return None

    def getall(self) -> pd.DataFrame:
        """Returns all data in the repository."""

        return super().getall(dtypes=DATAFRAME_DTYPES)

    def update(self, request: ReviewRequest) -> None:
        """Updates a request in the repository

        Args:
            request (ReviewRequest): Object containing details of the review HTTP request.
        """
        try:
            exists = self.exists(id=request.id)
        except Exception:
            exists = False

        if exists:
            query = f"""UPDATE {self._name} SET last_index=:last_index WHERE id =:id;"""
            params = {"id": request.id, "last_index": request.last_index}
            self._database.update(query=query, params=params)
        else:
            msg = f"Request for id: {request.id} does not exist."
            self._logger.exception(msg)
            raise ValueError(msg)

    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """
        self._database.insert(
            data=data, tablename=self._name, dtype=DATABASE_DTYPES, if_exists="replace"
        )
        msg = f"Replace {self._name} repository data with {data.shape[0]} rows."
        self._logger.debug(msg)

    def upsert(self, request: ReviewRequest) -> None:
        """Updates the request or inserts it if it doesn't exist.

        Args:
            request (ReviewRequest): Object containing the review request index.
        """
        if self.exists(id=request.id):
            self.update(request=request)
        else:
            self.add(request=request)

    @property
    def summary(self) -> pd.DataFrame:
        """Summarizes the requests by category"""
        df = self.getall()
        return df.groupby(["category_id"])["id"].nunique().to_frame()
