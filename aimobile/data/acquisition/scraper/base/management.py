#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/scraper/base/management.py                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 09:04:09 am                                                #
# Modified   : Saturday April 29th 2023 11:10:08 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from typing import Union
from datetime import datetime

import pandas as pd

# ------------------------------------------------------------------------------------------------ #
IMMUTABLE_TYPES: tuple = (str, int, float, bool, type(None))
SEQUENCE_TYPES: tuple = (list, tuple)


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Event(ABC):
    def as_dict(self) -> dict:
        """Returns a dictionary representation of the the Config object."""
        return {k: self._export_config(v) for k, v in self.__dict__.items()}

    @classmethod
    def _export_config(cls, v):
        """Returns v with Configs converted to dicts, recursively."""
        if isinstance(v, IMMUTABLE_TYPES):
            return v
        elif isinstance(v, SEQUENCE_TYPES):
            return type(v)(map(cls._export_config, v))
        elif isinstance(v, datetime):
            return v.strftime("%H:%M:%S on %m/%d/%Y")
        elif isinstance(v, dict):
            return v
        elif hasattr(v, "as_dict"):
            return v.as_dict()
        else:
            """Else nothing. What do you want?"""

    def as_df(self) -> pd.DataFrame:
        """Returns the project in DataFrame format"""
        d = self.as_dict()
        return pd.DataFrame.from_dict(data=d, orient="columns")


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Project(Event):
    id: Union[str, int]
    controller: str
    term: str
    state: str
    pages: int
    start_page: int
    end_page: int = None
    ended: datetime = None

    @classmethod
    def create(
        cls, id: Union[int, str], controller: str, term: str, start_page: int, pages: int
    ) -> Project:
        return cls(
            id=id,
            controller=controller,
            term=term,
            pages=pages,
            start_page=start_page,
            end_page=start_page + pages,
            ended=datetime.now(),
            state="complete",
        )


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Task(Event):
    id: Union[str, int]
    controller: str
    term: str
    app_id: int
    page: int
    completed: datetime = None

    @classmethod
    def create(
        cls, id: Union[int, str], controller: str, term: str, app_id: int, page: int
    ) -> Task:
        """Creates a Task object"""
        return cls(
            id=id,
            controller=controller,
            term=term,
            app_id=app_id,
            page=page,
            completed=datetime.now(),
        )
