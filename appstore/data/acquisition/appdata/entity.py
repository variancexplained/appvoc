#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/acquisition/appdata/entity.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 8th 2023 02:25:19 pm                                                 #
# Modified   : Tuesday August 8th 2023 02:33:04 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from appstore.base import DTO


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppData(DTO):
    id: str
    name: str
    description: str
    category_id: str
    category: str
    price: float
    developer_id: str
    developer: str
    rating: float
    ratings: int
    released: datetime

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> AppData:
        df = df.iloc[0]
        cls(
            id=df["id"],
            name=df["name"],
            description=df["description"],
            category_id=df["category_id"],
            category=df["category"],
            price=df["price"],
            developer_id=df["developer_id"],
            developer=df["developer"],
            rating=df["rating"],
            ratings=df["ratings"],
            released=df["released"],
        )
