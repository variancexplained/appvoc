#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/base/task.py                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday April 28th 2023 10:50:00 pm                                                  #
# Modified   : Saturday April 29th 2023 06:56:05 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

import pandas as pd


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Task:
    id: str
    Project: str
    searchagory: str
    start_page: int = 0
    end_page: int = 0
    pages: int = 0
    started: datetime = None
    updated: datetime = None
    ended: datetime = None
    state: str = "ready"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}\n\tId: {self.id}\n\tProject: {self.Project}\n\tSearchagory: {self.searchagory}\
        \n\tScrapers: {self.pages}\n\tState: {self.state}\n\tStarted: {self.started}\n\tUpdated: {self.updated}\n\tEnded: {self.ended}"

    def __repr__(self) -> str:  # pragma: no cover
        return f"{self.__class__.__name__}.{self.id}.{self.host}.{self.Project}.{self.searchagory}\
        .{self.pages}.{self.state}.{self.started}.{self.updated}.{self.ended}"

    def start(self, start_page: int = 0) -> None:
        self.started = datetime.now()
        self.start_page = start_page
        self.state = "in-progress"

    def update(self, pages: int) -> None:
        self._end_page = pages + self.start_page
        self.pages = pages
        self.updated = datetime.now()

    def complete(self) -> None:
        self.state = "complete"
        self.updated = datetime.now()
        self.ended = datetime.now()

    def to_df(self) -> pd.DataFrame:
        d = {
            "id": self.id,
            "Project": self.Project,
            "searchagory": self.searchagory,
            "pages": self.pages,
            "state": self.state,
            "started": self.started,
            "updated": self.updated,
            "ended": self.ended,
        }
        return pd.DataFrame(data=d, index=[0])

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> Task:
        d = df.to_dict(orient="records", index=True)
        if isinstance(d, list):
            d = d[0]

        return cls(
            id=d["id"],
            Project=d["Project"],
            searchagory=d["searchagory"],
            started=d["started"],
            updated=d["updated"],
            pages=d["pages"],
            state=d["state"],
            ended=d["ended"],
        )
