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
# Modified   : Wednesday August 2nd 2023 12:36:13 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Result Object for Rating Responses"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

import requests

from appstore.data.acquisition.base import Result, App
from appstore.infrastructure.web.utils import getsize


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

    app: App = None
    reviews: int = 0

    def add_response(self, response: requests.Response, app: App) -> None:
        """Adds a response to the instance

        Args:
           response (requests.Response): HTTP Response
        """
        self.app = app

        self.size += getsize(response=response)

        for data in response.json()["userReviewList"]:
            review = self._parse_review(data=data)
            if review is not None:
                self.content.append(review)

    def _parse_review(self, data: dict) -> dict:
        keys = [
            "userReviewId",
            "name",
            "rating",
            "title",
            "body",
            "voteSum",
            "voteCount",
            "date",
        ]

        review = {}
        review["id"] = self.app.id
        review["name"] = self.app.name
        review["category_id"] = self.app.category_id
        review["category"] = self.app.category

        for key in keys:
            try:
                if key == "date":
                    review[key] = datetime.strptime(data[key], "%Y-%m-%dT%H:%M:%f%z")
                else:
                    review[key] = data[key]
            except KeyError as e:
                msg = f"Exception occurred: Review data is missing the {key} value.\n{e}"
                self._logger.debug(msg)
                self.errors += 1
                return None
        self.reviews += 1
        return review
