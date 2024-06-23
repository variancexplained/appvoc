#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/data/repo/base.py                                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 11:34:11 am                                                  #
# Modified   : Wednesday August 30th 2023 07:22:16 pm                                              #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module provides basic database interface"""
from __future__ import annotations
import os
from datetime import datetime
import logging
from abc import ABC, abstractmethod
from typing import Union

from dotenv import load_dotenv
import pandas as pd

from appvoc.infrastructure.database.base import Database
from appvoc.infrastructure.file.io import IOService
from appvoc.infrastructure.file.config import FileConfig

# ------------------------------------------------------------------------------------------------ #
load_dotenv()


# ------------------------------------------------------------------------------------------------ #
class Repo(ABC):
    """Provides base class for all repositories classes.

    Args:
        name (str): Repository name. This will be the name of the underlying database table.
        database(Database): Database containing data to access.
    """

    def __init__(self, name: str, database: Database, config=FileConfig) -> None:
        self._name = name
        self._database = database
        self._config = config()
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @abstractmethod
    def load(self, data: pd.DataFrame) -> None:
        """Adds the dataframe rows to the designated table.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """

    @abstractmethod
    def replace(self, data: pd.DataFrame) -> None:
        """Replaces the data in a repository with that of the data parameter.

        Args:
            data (pd.DataFrame): DataFrame containing rows to add to the table.
        """

    def reset(self, force: bool = False) -> None:
        """Resets the repository by dropping the underlying table."""
        query = f"DROP TABLE IF EXISTS {self._name};"
        params = None
        x = "NO"
        if not force:
            x = input(
                "This will delete the underlying table and commit the database. Type 'YES' to proceed."
            )
        if force is True or x == "YES":
            self._database.execute(query=query, params=params)
            self.save()
            msg = f"Repository {self.__class__.__name__} reset."
            self._logger.info(msg)

    def sample(
        self,
        n: int = 5,
        frac: float = None,
        category_id: str = None,
        random_state: int = None,
    ) -> pd.DataFrame:
        """Returns a random sample from the underlying dataset.

        Args:
            n (int): Number of samples to return. Optional, defaults to 1.
            frac (float): Proportion of the data to return. n is ignored
                if this variable is non-null. Optional
            category_id (str): Four character category_id. Optional
            random_state (int): Seed for pseudo random generation.
        """
        if category_id is None:
            df = self.getall()
        else:
            df = self.get_by_category(category_id=category_id)
        return df.sample(n=n, frac=frac, random_state=random_state)

    def info(self) -> pd.DataFrame:
        """Wrapper for pandas info method"""
        df = self.getall()
        df.info()

    def get(
        self,
        id: Union[str, int],
        dtypes: dict = None,
        parse_dates: dict = None,
    ) -> pd.DataFrame:  # noqa
        """Returns data for the entity designated by the 'id' parameter.

        Args:
            id (Union[str,int]): The entity id.
            dtypes (dict): Dictionary mapping of column to data types
            parse_dates (dict): Dictionary of columns and keyword arguments for datetime parsing.
        """

        query = f"SELECT * FROM {self._name} WHERE id = :id;"
        params = {"id": id}
        return self._database.query(
            query=query, params=params, dtypes=dtypes, parse_dates=parse_dates
        )

    def get_by_category(
        self,
        category_id: Union[str, int],
        dtypes: dict = None,
        parse_dates: dict = None,
    ) -> pd.DataFrame:
        """Obtains data from the given table by category id

        Args:
            category_id (Union[str,int]): The mobile app category.
            dtypes (dict): Dictionary mapping of column to data types
            parse_dates (dict): Dictionary of columns and keyword arguments for datetime parsing.
        """
        query = f"SELECT * FROM {self._name} WHERE category_id = :category_id;"
        params = {"category_id": category_id}
        return self._database.query(
            query=query, params=params, dtypes=dtypes, parse_dates=parse_dates
        )

    def getall(self, dtypes: dict = None, parse_dates: dict = None) -> pd.DataFrame:
        """Returns all data in the repository.

        Args:
            dtypes (dict): Dictionary mapping of column to data types
            parse_dates (dict): Dictionary of columns and keyword arguments for datetime parsing.
        """
        query = f"SELECT * FROM {self._name};"
        params = None
        return self._database.query(
            query=query, params=params, dtypes=dtypes, parse_dates=parse_dates
        )

    def exists(self, id: Union[str, int]) -> bool:  # noqa
        """Assesses the existence of an entity in the database.

        Args:
            id (Union[str,int]): The app id.
        """
        query = f"SELECT EXISTS(SELECT 1 FROM {self._name} WHERE id = :id);"
        params = {"id": id}
        return self._database.exists(query=query, params=params)

    def count(self, id: Union[str, int] = None) -> int:  # noqa
        """Counts the entities matching the criteria. Counts all entities if id is None.

        Args:
            id (Union[str,int]): Entity id

        Returns number of rows matching criteria
        """
        if id is not None:
            query = f"SELECT * FROM {self._name} WHERE id = :id;"
            params = {"id": id}
        else:
            query = f"SELECT * FROM {self._name};"
            params = {}

        return self._database.query(query=query, params=params).shape[0]

    def delete(self, id: Union[str, int]) -> int:  # noqa
        """Deletes the entity designated by the id.

        Args:
            id (Union[str,int]): Entity id

        """
        query = f"DELETE FROM {self._name} WHERE id = :id;"
        params = {"id": id}
        self._database.delete(query=query, params=params)
        self.save()

    def delete_by_category(self, category_id: Union[str, int]) -> int:
        """Deletes the entities by category_id

        Args:
            category_id (Union[str,int]): Category identifier.

        """
        query = f"DELETE FROM {self._name} WHERE category_id = :category_id;"
        params = {"category_id": category_id}
        self._database.delete(query=query, params=params)
        self.save()

    def delete_all(self) -> int:
        """Deletes all entities from the repository."""

        query = f"DELETE FROM {self._name};"
        params = {}
        self._database.delete(query=query, params=params)
        self.save()

    def get_duplicates(self, by: str = "id") -> pd.DataFrame:
        """Returns duplicate rows examing the column or columns in 'by'.

        Args:
            by (str,list): A variable or list of variables in the repository.
        """
        df = self.getall()
        counts = (
            df[by]
            .value_counts(sort=True, ascending=False, normalize=False)
            .reset_index()
        )
        counts

    def dedup(self, keep: str = "last", subset: str = "id") -> None:
        """Removes duplicates by id"""
        df = self.getall()
        n1 = df.shape[0]
        df = df.drop_duplicates(subset=subset, keep=keep)
        n2 = df.shape[0]
        r = n1 - n2
        self.replace(data=df)
        self.save()
        msg = f"Repository with {n1} observations dropped {r} duplicates leaving {n2} observations"
        self._logger.info(msg)

    def save(self) -> None:
        """Saves the repository to file located in the designated directory."""
        self._database.commit()

    def export(
        self,
        directory: str = None,
        format: str = "pkl",
        by_category: bool = False,
        with_datetime: bool = True,
    ) -> str:
        """Archives the data
        Args:
            directory (str): The base directory into which the archive is created.
                Optional. Defaults to the archive directory in an environment
                variable.
        """
        df = self.getall()
        if directory is None:
            basedir = self._config.datasets
            directory = os.path.join(basedir, self._name)

        if with_datetime:
            name = self._name + "_" + datetime.now().strftime("%Y-%m-%dT%H%M%S")
        else:
            name = self._name

        os.makedirs(directory, exist_ok=True)
        if by_category:
            filepath = []
            for category, data in df.groupby(by="category"):
                filename = name + "_" + category + "." + format
                fp = os.path.join(directory, filename)
                filepath.append(fp)
                IOService.write(filepath=fp, data=data)
        else:
            filename = name + "." + format
            filepath = os.path.join(directory, filename)
            IOService.write(filepath=filepath, data=df)
        return filepath

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
