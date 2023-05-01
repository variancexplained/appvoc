#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/project.py                                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 03:47:36 pm                                                  #
# Modified   : Sunday April 30th 2023 07:43:13 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass, field
import itertools
from datetime import datetime

import pandas as pd

# ------------------------------------------------------------------------------------------------ #
IMMUTABLE_TYPES: tuple = (str, int, float, bool, type(None))
SEQUENCE_TYPES: tuple = (list, tuple)
# ------------------------------------------------------------------------------------------------ #
counter = itertools.count()
# ------------------------------------------------------------------------------------------------ #


@dataclass
class Project:
    host: str
    controller: str
    term: str
    status: str = "ready"
    start_page: int = 0
    end_page: int = 0
    pages: int = 0
    results_per_page: int = 0
    started: datetime = None
    updated: datetime = None
    completed: datetime = None
    id: int = field(default_factory=lambda: next(counter))

    @classmethod
    def start(
        cls,
        controller: str,
        term: str,
        start_page: int,
        host: str = "itunes.apple.com",
        results_per_page: int = 200,
    ) -> None:
        """Creates a Project object

        Args:
            controller (str): The name of the controller object.
            term (str): The term or category used as search term.
            start_page (str): The first page to be requested.
        """
        return cls(
            host=host,
            controller=controller,
            term=term,
            start_page=start_page,
            started=datetime.now(),
            status="running",
            results_per_page=results_per_page,
        )

    def update(self, pages: int) -> None:
        """Updates the current Project end page and pages elements."""
        self.end_page = self.start_page + pages
        self.pages = pages
        self.updated = datetime.now()

    def complete(self) -> None:
        """Changes the status to complete and sets the datetime."""
        self.state = "complete"
        self.completed = datetime.now()

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> Project:
        """Takes a DataFrame and creates a Project object."""
        return cls(
            host=df["host"][0],
            controller=df["controller"][0],
            term=df["term"][0],
            status=df["status"][0],
            start_page=df["start_page"][0],
            end_page=df["end_page"][0],
            pages=df["pages"][0],
            results_per_page=df["results_per_page"][0],
            started=df["started"][0],
            updated=df["updated"][0],
            completed=df["completed"][0],
        )

    def as_dict(self) -> dict:
        """Returns a dictionary representation of the the Config object."""
        return {k: self._export_config(v) for k, v in self.__dict__.items()}

    @classmethod
    def _export_config(cls, v):  # pragma: no cover
        """Returns v with Configs converted to dicts, recursively."""
        if isinstance(v, IMMUTABLE_TYPES):
            return v
        elif isinstance(v, SEQUENCE_TYPES):
            return type(v)(map(cls._export_config, v))
        elif isinstance(v, datetime):
            return v
        elif isinstance(v, dict):
            return v
        elif hasattr(v, "as_dict"):
            return v.as_dict()
        else:
            """Else nothing. What do you want?"""

    def as_df(self) -> pd.DataFrame:
        """Returns the project in DataFrame format"""
        d = self.as_dict()
        return pd.DataFrame(data=d, index=[0])
