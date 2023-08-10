#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/acquisition/review/request.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday August 9th 2023 04:52:24 pm                                               #
# Modified   : Wednesday August 9th 2023 07:05:53 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass

import pandas as pd
from appstore.base import DTO


# ------------------------------------------------------------------------------------------------ #
@dataclass
class ReviewRequest(DTO):
    id: str = None
    category_id: str = None
    last_index: int = 0

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> ReviewRequest:
        df = df.loc[0]
        return cls(id=df["id"], category_id=df["category_id"], last_index=df["last_index"])
