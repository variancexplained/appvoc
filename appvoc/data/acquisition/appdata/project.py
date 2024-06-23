#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/data/acquisition/appdata/project.py                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 03:47:36 pm                                                  #
# Modified   : Tuesday August 29th 2023 07:17:14 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass, field
import itertools
from datetime import datetime

import pandas as pd
from appvoc.data.acquisition.base import Project

# ------------------------------------------------------------------------------------------------ #

# ------------------------------------------------------------------------------------------------ #
counter = itertools.count()


# ------------------------------------------------------------------------------------------------ #
#                                       APP DATA PROJECT                                           #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppDataProject(Project):
    controller: str
    term: str
    status: str = "ready"
    page_size: int = 200
    pages: int = 0
    vpages: int = 0
    apps: int = 0
    started: datetime = None
    updated: datetime = None
    completed: datetime = None
    id: int = field(default_factory=lambda: next(counter))  # noqa

    def __len__(self):
        return 1

    @classmethod
    def start(
        cls,
        controller: str,
        term: str,
        page_size: int = 200,
    ) -> None:
        """Creates a Project object

        Args:
            controller (str): The name of the controller object.
            term (str): The term or category used as search term.
            page_size (int): Number of results to return per page.
        """
        return cls(
            controller=controller,
            term=term,
            page_size=page_size,
            pages=0,
            vpages=0,
            apps=0,
            started=datetime.now(),
            status="in-progress",
        )

    def update(self, apps: int) -> None:
        """Updates the current Project each page."""
        self.pages += 1
        self.apps += apps
        self.vpages = int(self.apps / self.page_size)
        self.updated = datetime.now()

    def complete(self) -> None:
        """Changes the status to complete and sets the datetime."""
        self.status = "complete"
        self.completed = datetime.now()

    def get_start_page(self) -> int:
        """Computes the start page based upon app count and max_result size"""
        return int(int(self.apps) / int(self.page_size))  # 200 results per page.

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> Project:
        """Takes a DataFrame and creates a Project object."""
        return cls(
            id=df["id"][0],
            controller=df["controller"][0],
            term=df["term"][0],
            status=df["status"][0],
            page_size=df["page_size"][0],
            pages=df["pages"][0],
            vpages=df["vpages"][0],
            apps=df["apps"][0],
            started=df["started"][0],
            updated=df["updated"][0],
            completed=df["completed"][0],
        )
