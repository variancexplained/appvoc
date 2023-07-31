#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/rating/result.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 01:59:31 pm                                                  #
# Modified   : Monday July 31st 2023 05:17:22 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Result Object for Rating Responses"""
from __future__ import annotations
from dataclasses import dataclass, field

import pandas as pd
from appstore.data.acquisition.base import Result


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RatingResult(Result):
    response: list[dict] = field(default_factory=list)
    apps: int = 0
    size: int = 0
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    status: bool = True

    def as_df(self) -> pd.DataFrame:
        """Returns the RatingResult(s) as a dataframe"""
        return pd.DataFrame(self.response)
