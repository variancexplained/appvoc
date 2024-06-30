#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/domain/review/review.py                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday August 10th 2023 11:46:15 pm                                               #
# Modified   : Saturday June 29th 2024 11:51:21 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from appvoc.domain.entity import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Review(Entity):
    """Encapsulates a review for an app."""

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
    def from_dict(cls, review: dict) -> Review:
        return cls(
            id=review["id"],
            app_id=review["app_id"],
            app_name=review["app_name"],
            category_id=review["category_id"],
            category=review["category"],
            author=review["author"],
            rating=review["rating"],
            title=review["title"],
            content=review["content"],
            vote_sum=review["vote_sum"],
            vote_count=review["vote_count"],
            date=pd.to_datetime(review["date"]),
        )
