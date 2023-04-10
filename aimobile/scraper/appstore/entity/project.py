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
# Modified   : Monday April 10th 2023 04:07:55 am                                                  #
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
    content_length: int = 0  # The total number of bytes received.
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
            and self.content_length == other.content_length
            and self.state == other.state
            and self.source == other.source
            and self.id == other.id
        )

    def __repr__(self) -> str:
        return f"{self.__module__}.{self.__class__.__name__}.{self.source} {self.name}: app_count={self.app_count}, page_count={self.page_count}, content_length={self.content_length}, started={self.started}, ended={self.ended}, duration={self.duration}, state={self.state}"

    def __str__(self) -> str:
        return f"Name: {self.name}:\n\tApp Count: {self.app_count}\n\tPage Count: {self.page_count}\n\tContent Length: {self.content_length}\n\tStarted: {self.started}\n\tEnded: {self.ended}\n\tDuration: {self.duration}\n\tState: {self.state}"

    def start(self) -> None:
        """Initialization"""
        self.app_count = 0
        self.page_count = 0
        self.content_length = 0
        self.started = datetime.now()

    def end(self) -> None:
        """Finalizes the project state"""
        self.ended = datetime.now()
        self.duration = (self.ended - self.started).total_seconds()
        self.state = "success" if self.state == "in-progress" else self.state

    def update(self, num_results: int, content_length: int) -> None:
        """Updates the Project with current app_count and page_count.

        The datetime variables are set and stored in the database on each
        scrape iteration, so that we know how far we have processed
        the data in the event an exception occurs.

        Args:
            num_results (int): The number of apps returned from the appstore.

        """
        self.app_count += num_results
        self.page_count += 1
        self.content_length += content_length
        # Snapshot
        self.started = datetime.now() if self.started == "" else self.started
        self.ended = datetime.now()
        self.duration = (self.ended - self.started).total_seconds()
        self.state = "in-progress" if self.state != "fail" else self.state

    @classmethod
    def from_df(cls, data: pd.DataFrame) -> AppStoreProject:
        return cls(
            id=int(data["id"]),
            name=data["name"],
            app_count=int(data["app_count"]),
            page_count=int(data["page_count"]),
            content_length=int(data["content_length"]),
            started=data["started"],
            ended=data["ended"],
            duration=int(data["duration"]),
            state=data["state"],
            source=data["source"],
        )
