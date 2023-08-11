#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/entity/review.py                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday August 10th 2023 11:46:15 pm                                               #
# Modified   : Friday August 11th 2023 01:04:49 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from appstore.base import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Review(Entity):
    id: str
    app_id: str
    app_name: str
    category_id: str
    category: str
    author: str
    rating: float
    title: str
    content: str
    vote_sum: int
    vote_count: int
    date: datetime

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> Review:
        df = df.iloc[0]
        return cls(
            id=df["id"],
            app_id=df["app_id"],
            app_name=df["app_name"],
            category_id=df["category_id"],
            category=df["category"],
            author=df["author"],
            rating=df["rating"],
            title=df["title"],
            content=df["content"],
            vote_sum=df["vote_sum"],
            vote_count=df["vote_count"],
            date=pd.to_datetime(df["date"]),
        )
