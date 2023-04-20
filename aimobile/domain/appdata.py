#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/domain/appdata.py                                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 2nd 2023 08:43:21 pm                                                   #
# Modified   : Thursday April 20th 2023 01:03:53 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union

import pandas as pd

from aimobile.domain.base import Entity
from aimobile.domain.review import Review


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppData(Entity):
    """Entity housing basic App definition data, such as name, title, price, etc..."""

    id: Union[str, int] = None  # App id
    name: str = None
    description: str = None
    category_id: int = None
    category: str = None
    price: float = None
    rating: float = None
    star_1: int = None
    star_2: int = None
    star_3: int = None
    star_4: int = None
    star_5: int = None
    ratings: int = None
    reviews: int = None
    developer_id: int = None
    developer: str = None
    released: str = None
    source: str = None
    _reviews: dict = field(default_factory=dict)

    def __eq__(self, other: AppData) -> bool:
        return (
            self.id == other.id
            and self.name == other.name
            and self.description == other.description
            and self.category_id == other.category_id
            and self.category == other.category
            and self.price == other.price
            and self.rating == other.rating
            and self.star_1 == other.star_1
            and self.star_2 == other.star_2
            and self.star_3 == other.star_3
            and self.star_4 == other.star_4
            and self.star_5 == other.star_5
            and self.ratings == other.ratings
            and self.reviews == other.reviews
            and self.developer_id == other.developer_id
            and self.developer == other.deverloper
            and self.released == other.released
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
            name=data["name"],
            description=data["description"],
            category_id=int(data["category_id"]),
            category=data["category"],
            price=float(data["price"]),
            rating=float(data["rating"]),
            star_1=int(data["star_1"]),
            star_2=int(data["star_2"]),
            star_3=int(data["star_3"]),
            star_4=int(data["star_4"]),
            star_5=int(data["star_5"]),
            ratings=int(data["ratings"]),
            reviews=int(data["reviews"]),
            developer_id=int(data["developer_id"]),
            developer=data["developer"],
            released=data["released"],
            source=data["source"],
        )
