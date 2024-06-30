#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.14                                                                             #
# Filename   : /appvoc/domain/repo.py                                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday June 30th 2024 12:29:05 am                                                   #
# Modified   : Sunday June 30th 2024 02:06:47 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
"""Repository Interface Module"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Union

import pandas as pd

from appvoc.domain.entity import Entity


# ------------------------------------------------------------------------------------------------ #
class Repo(ABC):
    """Provides base class for all repositories classes."""

    @abstractmethod
    def reset(self) -> None:
        """Resets the repository, deleting all rows."""

    @abstractmethod
    def add(self, entity: Entity) -> None:
        """Adds an entity to the repository.

        Args:
            entity (Entity): Entity to be added
        """

    @abstractmethod
    def load(self, df: pd.DataFrame) -> None:
        """Loads a dataframe containing entity data into the repository.

        Args:
            df (pd.DataFrame): DataFrame containing entity information.
        """

    @abstractmethod
    def findby(self, condition: Callable) -> pd.DataFrame:
        """Finds multiple entities meeting a condition

        Args:
            condition (Callable): Lambda expression that can be used to subset a
                DataFrame. Optional.
        """

    @abstractmethod
    def findall(self) -> pd.DataFrame:
        """Returns all entties from repository in a DataFrame format."""

    @abstractmethod
    def exists(self, id: Union[str, int]) -> bool:  # noqa
        """Assesses the existence of an entity in the database.

        Args:
            id (Union[str,int]): The app id.
        """

    @abstractmethod
    def count(self, condition: Callable = None) -> int:  # noqa
        """Counts the entities matching the criteria. Counts all entities if condition is None.

        Args:
            condition (Callable): Lambda expression that can be used to subset a
                DataFrame. Optional.

        Returns number of rows matching criteria
        """

    @abstractmethod
    def remove(self, id: Union[str, int]) -> int:  # noqa
        """Deletes the entity designated by the id.

        Args:
            id (Union[str,int]): Entity id

        """

    @abstractmethod
    def removeby(self, condition: Callable) -> int:
        """Deletes the entities by category_id

        Args:
            condition (Callable): Lambda expression that can be used to subset a
                DataFrame. Optional.

        """

    @abstractmethod
    def save(self) -> None:
        """Commits the repository."""

    def _parse_datetime(
        self, data: pd.DataFrame, dtcols: Union[str, list[str]]
    ) -> pd.DataFrame:
        """Converts strings to datetime objects for the designated column.

        Args:
            data (pd.DataFrame): Data containing datetime columns
            dtcols ( Union[str, list[str]]): Columns or column containing datetime or string datetime data.
        """
        if isinstance(dtcols, str):
            dtcols = [dtcols]
        for dtcol in dtcols:
            if pd.api.types.is_string_dtype(data[dtcol].dtype):
                data[dtcol] = pd.to_datetime(data[dtcol])
        return data


# ------------------------------------------------------------------------------------------------ #
#                                       UNIT OF WORK CLASS                                         #
# ------------------------------------------------------------------------------------------------ #
class UnitOfWork:
    """Unit of Work ABC class defining the interface for unit of work classes."""

    @abstractmethod
    @property
    def app_repo(self) -> Repo:
        """Returns the AppRepo"""

    @abstractmethod
    @property
    def review_repo(self) -> Repo:
        """Returns the ReviewRepo"""

    @abstractmethod
    @property
    def rating_repo(self) -> Repo:
        """Returns the RatingRepo"""

    @abstractmethod
    @property
    def job_repo(self) -> Repo:
        """Returns the JobRepo"""

    @abstractmethod
    @property
    def app_jobrun_repo(self) -> Repo:
        """Returns the AppJobRunRepo"""

    @abstractmethod
    @property
    def rating_jobrun_repo(self) -> Repo:
        """Returns the RatingJobRunRepo"""

    @abstractmethod
    @property
    def review_jobrun_repo(self) -> Repo:
        """Returns the ReviewJobRunRepo"""

    @abstractmethod
    @property
    def connect(self) -> None:
        """Connects the database"""

    @abstractmethod
    @property
    def begin(self) -> None:
        """Begin a transaction"""

    @abstractmethod
    @property
    def save(self) -> None:
        """Saves changes to the underlying sqlite context"""

    @abstractmethod
    @property
    def rollback(self) -> None:
        """Returns state of sqlite to the point of the last commit."""

    @abstractmethod
    @property
    def close(self) -> None:
        """Closes the sqlite connection."""
