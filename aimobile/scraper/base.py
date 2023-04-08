#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/scraper/base.py                                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 3rd 2023 12:36:15 am                                                   #
# Modified   : Saturday April 8th 2023 02:55:57 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Base classes shared by both appstore and google scraping services."""
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import dataclass
from typing import Union

import pandas as pd

# ------------------------------------------------------------------------------------------------ #
IMMUTABLE_TYPES: tuple = (str, int, float, bool, type(None))
SEQUENCE_TYPES: tuple = (list, tuple)


# ------------------------------------------------------------------------------------------------ #
#                                  ABSTRACT SCRAPER FACTORY                                        #
# ------------------------------------------------------------------------------------------------ #
class AbstractScraperFactory(ABC):
    """Defines a factory interface with methods that return abstract appdata and review scrapers"""

    @abstractmethod
    def create_appdata_scraper(self) -> AbstractAppDataScraper:
        """Returns a concrete AppDataScraper

        Args:
            project (AbtractScraperProject): Object defining the projecturation for the scraper.
        """

    @abstractmethod
    def create_review_scraper(self) -> AbstractReviewScraper:
        """Returns a concrete ReviewScraper

        Args:
            project (AbtractScraperProject): Object defining the projecturation for the scraper.
        """


# ------------------------------------------------------------------------------------------------ #
#                              ABSTRACT APPDATA SCRAPER                                            #
# ------------------------------------------------------------------------------------------------ #
class AbstractAppDataScraper(ABC):
    """Defines the interface for app data scrapers."""

    def search(self, term) -> None:
        """Executes a search of app data, and persists the results in an appdate repository.

        Args:
            term (str): Search term.

        """


# ------------------------------------------------------------------------------------------------ #
#                              ABSTRACT REVIEW SCRAPER                                             #
# ------------------------------------------------------------------------------------------------ #
class AbstractReviewScraper(ABC):
    """Defines the interface for review scrapers."""


# ------------------------------------------------------------------------------------------------ #
#                                           REPO                                                   #
# ------------------------------------------------------------------------------------------------ #
class Repo(ABC):
    """Abstract base class for app data, review repositories."""

    @abstractmethod
    def get(self, id: int) -> Entity:
        """Queries the database and returns the entity indicated by the id.

        Args:
            id (int): The identifier for the entity

        Raises: EntityNotFound if the entity was not found.
        """

    @abstractmethod
    def getall(self, as_df: bool = True) -> Union[dict, pd.DataFrame]:
        """Returns a dictionary or DataFrame of all entities (of the type) in the repository

        Args:
            as_df (bool): If True, a pandas DataFrame is returned; otherwise, a dictionary
                where key is the entity id and value is the entity, is returned.

        raises EntityNotFound if the repository is empty.
        """

    @abstractmethod
    def add(self, data: Union[Entity, pd.DataFrame]) -> None:
        """Adds one ore more entities to the Database.

        Args:
            data (Union[Entity, pd.DataFrame]): If the type is Entity, a single instance
                of the entity is added to the database. If the tpye is pd.DataFrame,
                the DataFrame of entities is added.
        """

    @abstractmethod
    def update(self, entity: Entity) -> None:
        """Updates an existing Entity in the database.

        Args:
            entity (Entity): The entity to update.

        Raises: EntityNotFound if the entity was not found.
        """

    @abstractmethod
    def remove(self, id: int) -> None:
        """Removies an entity from the database based upon the entity id.

        Args:
            id (int): Id for the entity to be removed.

        Raises: EntityNotFound if the entity was not found.
        """


# ------------------------------------------------------------------------------------------------ #
#                                        ENTITY                                                    #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class Entity(ABC):
    """Abstract base class which defines the interface for entity classes."""

    def as_df(self) -> pd.DataFrame:
        """Returns the entity in DataFrame format."""
        d = self.as_dict()
        return pd.DataFrame(data=d, index=[0])

    def as_dict(self) -> dict:
        """Returns a dictionary representation of the the parameter object."""
        return {k: self._export_config(v) for k, v in self.__dict__.items()}

    @classmethod
    def _export_config(cls, v):
        """Returns v with Configs converted to dicts, recursively."""
        if isinstance(v, IMMUTABLE_TYPES):
            return v
        elif isinstance(v, SEQUENCE_TYPES):
            return type(v)(map(cls._export_config, v))
        elif isinstance(v, datetime):
            return v.strftime("%m/%d/%Y, %H:%M:%S")
        elif isinstance(v, dict):
            return {kk: cls._export_config(vv) for kk, vv in v}
        else:
            try:
                return v.__class__.__name__
            except:  # noqa 722
                return "Mutable Object"


# ------------------------------------------------------------------------------------------------ #
#                                  REQUEST ITERATOR                                                #
# ------------------------------------------------------------------------------------------------ #
class RequestIterator(ABC):
    """Encapsulates an HTTP request and response handling"""

    @abstractmethod
    def __iter__(self) -> RequestIterator:
        """Initializes the iterator and returns it."""

    @abstractmethod
    def __next__(self) -> pd.DataFrame:
        """Iterates a request and returns the result."""


# ------------------------------------------------------------------------------------------------ #
#                                         HANDLER                                                  #
# ------------------------------------------------------------------------------------------------ #
class Handler(ABC):
    """Abstract base class for HTTP Handlers."""
