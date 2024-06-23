#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/data/acquisition/review/result.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 01:59:31 pm                                                  #
# Modified   : Thursday August 31st 2023 11:49:50 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Result Object for Rating Responses"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

import requests
import pandas as pd

from appvoc.data.acquisition.base import Result, App
from appvoc.infrastructure.web.utils import getsize


# ------------------------------------------------------------------------------------------------ #
@dataclass
class ReviewResult(Result):
    """Encapsulates the review results. Inherits the following from Result base class:
    content (list): List of dictionaries containing the response content
    size: (int): Total size of response in bytes
    requests (int): Number of requests. This will be one for syncronous requests,
        async requests vary.
    successes: (int): Number of successful responses
    errors: (int): Number of errors.

    """

    content: List = field(default_factory=lambda: [])
    app: App = None
    reviews: int = 0
    index: int = 0

    def add_response(
        self, response: requests.Response, app: App, index: int = 0
    ) -> None:
        """Adds a response to the instance

        Args:
           response (requests.Response): HTTP Response
        """
        self.app = app
        self.index = index

        self.size += getsize(response=response)

        for data in response.json()["userReviewList"]:
            review = self._parse_review(data=data)
            if review is not None:
                self.content.append(review)

    def _parse_review(self, data: dict) -> dict:
        try:
            review = {}
            review["id"] = data["userReviewId"]
            review["app_id"] = self.app.id
            review["app_name"] = self.app.name
            review["category_id"] = self.app.category_id
            review["category"] = self.app.category
            review["author"] = data["name"]
            review["rating"] = data["rating"]
            review["title"] = data["title"]
            review["content"] = data["body"]
            review["vote_sum"] = data["voteSum"]
            review["vote_count"] = data["voteCount"]
            review["date"] = pd.to_datetime(data["date"])

        except Exception as e:
            msg = f"Exception of type {type(e)} occurred.\n{e}"
            self._logger.debug(msg)
            self.data_errors += 1
            return None
        else:
            self.reviews += 1
            return review
