#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/data/acquisition/review/request.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday August 9th 2023 04:52:24 pm                                               #
# Modified   : Thursday August 10th 2023 12:10:41 am                                               #
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
class ReviewRequest(Entity):
    id: str = None
    category_id: str = None
    last_index: int = 0

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> ReviewRequest:
        df = df.loc[0]
        return cls(
            id=df["id"], category_id=df["category_id"], last_index=df["last_index"]
        )
