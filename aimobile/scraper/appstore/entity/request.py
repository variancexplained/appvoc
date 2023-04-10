#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/entity/request.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 5th 2023 10:46:15 am                                                #
# Modified   : Monday April 10th 2023 02:31:46 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"Request Module: Defines the unit of work for scraping operations."
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from aimobile.scraper.base import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppStoreRequest(Entity):
    host: str
    name: str
    page: int
    content_length: int
    results: int
    requested: str  # Date time string
    responded: str  # Date time string
    response_time: float
    sessions: int
    proxy: str
    status_code: int
    id: int = None

    def __post_init__(self) -> None:
        if isinstance(self.requested, datetime):
            self.requested = self.requested.strftime("%m/%d/%Y %H:%M:%S")
        if isinstance(self.responded, datetime):
            self.responded = self.responded.strftime("%m/%d/%Y %H:%M:%S")

    def __eq__(self, other: AppStoreRequest) -> bool:
        return self.host == other.host and self.term == other.term and self.page == other.page

    @classmethod
    def from_df(cls, data: pd.DataFrame) -> AppStoreRequest:
        return cls(
            id=int(data["id"]),
            host=str(data["host"]),
            name=str(data["name"]),
            page=int(data["page"]),
            content_length=int(data["content_length"]),
            results=int(data["results"]),
            requested=data["requested"],
            responded=data["responded"],
            response_time=float(data["response_time"]),
            sessions=int(data["sessions"]),
            proxy=str(data["proxy"]),
            status_code=data["status_code"],
        )

    @classmethod
    def from_dict(cls, data: dict) -> AppStoreRequest:
        return cls(
            id=data.get("id", None),
            host=str(data.get("host", "")),
            name=str(data.get("name", "")),
            page=int(data.get("page", 0)),
            content_length=int(data.get("content_length", 0)),
            results=int(data.get("results", 0)),
            requested=data.get("requested", ""),
            responded=data.get("responded", ""),
            response_time=float(data.get("response_time", 0)),
            sessions=int(data.get("sessions", 1)),
            proxy=str(data.get("proxy", None)),
            status_code=data.get("status_code", 200),
        )
