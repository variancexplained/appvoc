#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/data/entity/appdata.py                                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday August 10th 2023 11:42:46 pm                                               #
# Modified   : Friday August 11th 2023 01:12:25 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from appvoc.base import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppData(Entity):
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
        return cls(
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
