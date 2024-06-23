#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/data/entity/rating.py                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday August 10th 2023 11:46:15 pm                                               #
# Modified   : Friday August 11th 2023 01:12:14 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass

import pandas as pd

from appvoc.base import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Rating(Entity):
    id: str
    name: str
    category_id: str
    category: str
    rating: float
    reviews: int
    ratings: int
    onestar: int
    twostar: int
    threestar: int
    fourstar: int
    fivestar: int

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> Rating:
        df = df.iloc[0]
        return cls(
            id=df["id"],
            name=df["name"],
            category_id=df["category_id"],
            category=df["category"],
            rating=df["rating"],
            reviews=df["reviews"],
            ratings=df["ratings"],
            onestar=df["onestar"],
            twostar=df["twostar"],
            threestar=df["threestar"],
            fourstar=df["fourstar"],
            fivestar=df["fivestar"],
        )
