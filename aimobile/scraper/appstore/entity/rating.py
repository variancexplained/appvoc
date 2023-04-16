#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/scraper/appstore/entity/rating.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 2nd 2023 08:43:21 pm                                                   #
# Modified   : Sunday April 16th 2023 03:28:40 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass

import pandas as pd

from aimobile.scraper.base import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppStoreRatings(Entity):
    id: int = None
    star_1: int = None
    star_2: int = None
    star_3: int = None
    star_4: int = None
    star_5: int = None
    total_ratings: int = None
    total_reviews: int = None
    source: str = None

    @classmethod
    def from_df(cls, data: pd.DataFrame) -> None:
        """Builds the Review object from the request and results

        Args:
            data (pd.DataFrame): Review data in pandas DataFrame format.
        """
        return cls(
            id=int(data["id"]),
            star_1=int(data["star_1"]),
            star_2=int(data["star_2"]),
            star_3=int(data["star_3"]),
            star_4=int(data["star_4"]),
            star_5=int(data["star_5"]),
            total_ratings=int(data["total_ratings"]),
            total_reviews=int(data["total_reviews"]),
            source=str(data["source"]),
        )

    @classmethod
    def from_dict(cls, data: dict) -> str:
        """Extracts the app_id from the review url

        Args:
            data (dict): Review data in dict format.
        """
        return cls.from_df(data=data)
