#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/entity/project.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 5th 2023 10:46:15 am                                                #
# Modified   : Monday April 10th 2023 02:13:26 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"Project Module: Defines the unit of work for scraping operations."
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from aimobile.scraper.base import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppStoreProject(Entity):
    name: str
    app_count: int = 0  # The number of apps returned
    page_count: int = 0  # The number of pages returned
    started: datetime = ""
    ended: datetime = ""
    duration: int = 0
    state: str = "not_started"
    source: str = "appstore"
    id: int = None

    def __eq__(self, other: AppStoreProject) -> bool:
        return (
            self.name == other.name
            and self.app_count == other.app_count
            and self.page_count == other.page_count
            and self.state == other.state
            and self.source == other.source
            and self.id == other.id
        )

    def __repr__(self) -> str:
        return f"{self.__module__}.{self.__class__.__name__}.{self.source} {self.name}: app_count={self.app_count}, page_count={self.page_count}, started={self.started}, ended={self.ended}, duration={self.duration}, state={self.state}"

    def __str__(self) -> str:
        return f"Name: {self.name}: App Count: {self.app_count}, Page Count: {self.page_count}, Started: {self.started}, Ended: {self.ended}, Duration: {self.duration}, State: {self.state}"

    def start(self) -> None:
        """Initialization"""
        self.app_count = 0
        self.page_count = 0
        self._started = datetime.now()
        self.started = self._started.strftime("%m/%d/%Y, %H:%M:%S")

    def end(self) -> None:
        """Finalizes the project state"""
        self._ended = datetime.now()
        self.ended = self._ended.strftime("%m/%d/%Y, %H:%M:%S")
        self.duration = (self._ended - self._started).total_seconds()
        self.state = "success" if self.state == "in-progress" else self.state

    def update(self, num_results: int) -> None:
        """Updates the Project with current app_count and page_count.

        The datetime variables are set and stored in the database on each
        scrape iteration, so that we know how far we have processed
        the data in the event an exception occurs.

        Args:
            num_results (int): The number of apps returned from the appstore.

        """
        self.app_count += num_results
        self.page_count += 1
        # Snapshot
        self._started = datetime.now() if self._started == "" else self._started
        self.started = self._started.strftime("%m/%d/%Y, %H:%M:%S")
        self._ended = datetime.now()
        self.ended = self._ended.strftime("%m/%d/%Y, %H:%M:%S")
        self.duration = (self._ended - self._started).total_seconds()
        self.state = "in-progress" if self.state != "fail" else self.state

    @classmethod
    def from_df(cls, data: pd.DataFrame) -> AppStoreProject:
        return cls(
            id=int(data["id"]),
            name=data["name"],
            app_count=int(data["app_count"]),
            page_count=int(data["page_count"]),
            started=data["started"],
            ended=data["ended"],
            duration=int(data["duration"]),
            state=data["state"],
            source=data["source"],
        )
