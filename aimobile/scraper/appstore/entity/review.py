#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/scraper/appstore/entity/review.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 2nd 2023 08:43:21 pm                                                   #
# Modified   : Monday April 10th 2023 11:01:33 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass

import pandas as pd

from aimobile.scraper.base import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppStoreReview(Entity):
    id: int = None
    app_id: int = None
    app_name: str = None
    category_id: int = None
    category: str = None
    author: str = None
    rating: float = None
    title: str = None
    content: str = None
    vote_sum: int = None
    vote_count: int = None
    date: str = None
    source: str = None

    @classmethod
    def from_df(cls, data: pd.DataFrame) -> None:
        """Builds the Review object from the request and results

        Args:
            result (dict): Results from HTTP request
            request (AbstractRequest): Contains the HTTP request parameters
        """
        return cls(
            id=data["id"],
            app_id=data["app_id"],
            app_name=data["app_name"],
            category_id=data["category_id"],
            category=data["category"],
            author=data["author"],
            rating=data["rating"],
            title=data["title"],
            content=data["content"],
            vote_sum=data["vote_sum"],
            vote_count=data["vote_count"],
            date=data["date"],
            source=data["source"],
        )

    @classmethod
    def from_dict(cls, data: dict) -> str:
        """Extracts the app_id from the review url

        Args:
            url (str): A URL for the itunes review, containing the app_id
        """
        return cls.from_df(data)
