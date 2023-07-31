#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/review/result.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 01:59:31 pm                                                  #
# Modified   : Monday July 31st 2023 01:09:30 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Result Object for Rating Responses"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import logging

import pandas as pd
from appstore.data.acquisition.base import Result, Response


# ------------------------------------------------------------------------------------------------ #
@dataclass
class ReviewResponse(Response):
    """Encapsulates a response from the ReviewScraper.

    Inherits the following member from the Response base class:
        status: bool = True
    """

    id: str = None  # noqa
    app_id: str = None
    app_name: str = None
    category_id: str = None
    category: str = None
    author: str = None
    rating: float = 0
    title: str = None
    content: str = None
    vote_sum: int = 0
    vote_count: int = 0
    date: datetime = None

    @classmethod
    def create(
        cls, app_id: str, app_name: str, category_id: str, category: str, response: dict
    ) -> ReviewResponse:
        """Factory method creating a ReviewResponse object

        Args:
            app_id (str): The application id for which the review was written
            app_name (str): The application name
            category_id (str): The four character Appstore category id
            category (str): The Appstore label
            response (dict): A dictionary containing a single review from the response object.
        """
        cls._logger = logging.getLogger(f"{cls.__class__.__name__}")

        try:
            review_response = cls(
                id=response["userReviewId"],
                app_id=app_id,
                app_name=app_name,
                category_id=category_id,
                category=category,
                author=response["name"],
                rating=float(response["rating"]),
                title=response["title"],
                content=response["body"],
                vote_sum=int(response["voteSum"]),
                vote_count=int(response["voteCount"]),
                date=datetime.strptime(response["date"], "%Y-%m-%dT%H:%M:%f%z"),
                status=True,
            )
            return review_response  # noqa

        except Exception as e:
            msg = f"\nInvalid response. Encountered {type(e)} exception.\n{e}\n{response}"
            cls._logger.debug(msg)

            # Create a failed response
            review_response = cls(
                app_id=app_id,
                app_name=app_name,
                category_id=category_id,
                category=category,
                status=False,
            )
            return review_response  # noqa


# ------------------------------------------------------------------------------------------------ #
@dataclass
class ReviewResult(Result):
    response: list[dict] = field(default_factory=list)
    apps: int = 1
    reviews: int = 0
    requests: int = 0
    successes: int = 0
    fails: int = 0

    def add_response(self, response: ReviewResponse) -> None:
        """Adds a response to the result object

        Args:
           response (ReviewResponse): An object encapsulating a single review response.
        """

        self.response.append(response.as_dict())
        self.requests += 1
        if response.status:
            self.reviews += 1
            self.successes += 1
        else:
            self.fails += 1

    def as_df(self) -> pd.DataFrame:
        """Returns the RatingResult(s) as a dataframe"""
        return pd.DataFrame(self.response)

    def is_valid(self) -> bool:
        """Assesses and returns Result validity"""
        return self.successes > 0
