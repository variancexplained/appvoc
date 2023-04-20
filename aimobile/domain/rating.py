#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/domain/rating.py                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 2nd 2023 08:43:21 pm                                                   #
# Modified   : Thursday April 20th 2023 07:36:28 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass
from typing import Union

import pandas as pd

from aimobile.domain.base import Entity
from aimobile.domain.review import Review


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppData(Entity):
    """Entity housing basic App definition data, such as name, title, price, etc..."""

    id: Union[str, int] = None  # App id
    star_1: int = None
    star_2: int = None
    star_3: int = None
    star_4: int = None
    star_5: int = None
    rating: int = None
    ratings: int = None
    source: str = None

    def __eq__(self, other: AppData) -> bool:
        return (
            self.id == other.id
            and self.star_1 == other.star_1
            and self.star_2 == other.star_2
            and self.star_3 == other.star_3
            and self.star_4 == other.star_4
            and self.star_5 == other.star_5
            and self.rating == other.rating
            and self.ratings == other.ratings
            and self.source == other.source
        )

    def add_review(self, review: Review) -> None:
        self._reviews[review.id] = review

    def get_review(self, review_id: Union[str, int]) -> Review:
        return

    @classmethod
    def from_dict(cls, data: pd.DataFrame) -> AppData:
        """Creates an AppData object from a dictionary."""
        return cls(
            id=int(data["id"]),
            star_1=int(data["star_1"]),
            star_2=int(data["star_2"]),
            star_3=int(data["star_3"]),
            star_4=int(data["star_4"]),
            star_5=int(data["star_5"]),
            rating=float(data["rating"]),
            ratings=int(data["ratings"]),
            source=data["source"],
        )
