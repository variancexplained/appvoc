#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/domain/rating/rating.py                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday August 10th 2023 11:46:15 pm                                               #
# Modified   : Saturday June 29th 2024 10:42:57 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations

from dataclasses import dataclass

from appvoc.domain.entity import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Rating(Entity):
    """Encapsulates rating data for an app"""

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
    def from_dict(cls, rating: dict) -> Rating:
        return cls(
            id=rating["id"],
            name=rating["name"],
            category_id=rating["category_id"],
            category=rating["category"],
            rating=rating["rating"],
            reviews=rating["reviews"],
            ratings=rating["ratings"],
            onestar=rating["onestar"],
            twostar=rating["twostar"],
            threestar=rating["threestar"],
            fourstar=rating["fourstar"],
            fivestar=rating["fivestar"],
        )
