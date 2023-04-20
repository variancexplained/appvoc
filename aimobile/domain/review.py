#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/domain/review.py                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 2nd 2023 08:43:21 pm                                                   #
# Modified   : Thursday April 20th 2023 12:41:24 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from dataclasses import dataclass

import pandas as pd

from aimobile.domain.base import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Review(Entity):
    id: int = None
    app_id: int = None
    author: str = None
    rating: float = None
    title: str = None
    content: str = None
    vote_sum: int = None
    vote_count: int = None
    date: str = None
    source: str = None

    def __eq__(self, other: Review) -> bool:
        return (
            self.id == other.id
            and self.app_id == other.app_id
            and self.author == other.author
            and self.rating == other.rating
            and self.title == other.title
            and self.content == other.content
            and self.vote_count == other.vote_count
            and self.date == other.date
            and self.source == other.source
        )

    @classmethod
    def from_dict(cls, data: pd.DataFrame) -> None:
        """Builds the Review object from the request and results

        Args:
            data (pd.DataFrame): Review data in pandas DataFrame format.
        """
        return cls(
            id=int(data["id"]),
            app_id=int(data["app_id"]),
            author=str(data["author"]),
            rating=float(data["rating"]),
            title=str(data["title"]),
            content=str(data["content"]),
            vote_sum=int(data["vote_sum"]),
            vote_count=int(data["vote_count"]),
            date=str(data["date"]),
            source=str(data["source"]),
        )
