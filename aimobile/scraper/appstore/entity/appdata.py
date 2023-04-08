#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/scraper/appstore/entity/appdata.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 2nd 2023 08:43:21 pm                                                   #
# Modified   : Saturday April 8th 2023 02:45:32 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass

import pandas as pd

from aimobile.scraper.base import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppStoreAppData(Entity):
    id: str = None
    name: str = None
    description: str = None
    category_id: int = None
    category: str = None
    price: float = None
    rating: float = None
    ratings: int = None
    developer_id: int = None
    developer: str = None
    released: str = None
    source: str = None

    def __eq__(self, other: AppStoreAppData) -> bool:
        return (
            self.id == other.id
            and self.name == other.name
            and self.description == other.description
            and self.category_id == other.category_id
            and self.category == other.category
            and self.price == other.price
            and self.rating == other.rating
            and self.ratings == other.ratings
            and self.developer_id == other.developer_id
            and self.developer == other.deverloper
            and self.released == other.released
            and self.source == other.source
        )

    @classmethod
    def from_df(cls, data: pd.DataFrame) -> AppStoreAppData:
        """Creates an AppStoreAppData object from a DataFrame."""
        return cls(
            id=int(data["id"]),
            name=data["name"],
            description=data["description"],
            category_id=int(data["category_id"]),
            category=data["category"],
            price=float(data["price"]),
            rating=float(data["rating"]),
            ratings=int(data["ratings"]),
            developer_id=int(data["developer_id"]),
            developer=data["developer"],
            released=data["released"],
            source=data["source"],
        )
