#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/data/acquisition/rating/result.py                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 01:59:31 pm                                                  #
# Modified   : Saturday June 29th 2024 10:25:52 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Response Object for Rating Responses"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from appvoc.data.acquisition.base import Response
from appvoc.infrastructure.web.utils import getsize


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RatingResponse(Response):
    """Encapsulates the review results. Inherits the following from Response base class:
    content: list[dict] = field(default_factory=list)
    size: int = 0
    data_errors: int = 0
    client_errors: int = 0
    server_errors: int = 0


    """

    content: List = field(default_factory=lambda: [])

    apps: int = 0

    def add_response(self, response: dict, batch: dict) -> None:
        """Adds a rating to the result content

        Args:
           review (dict): Dictionary containing review data
        """

        self.size += getsize(response)
        self.apps += 1

        id = str(response["adamId"])  # noqa
        page = {}
        page["id"] = [app["id"] for app in batch if app["id"] == id][0]
        page["name"] = [app["name"] for app in batch if app["id"] == id][0]
        page["category_id"] = [
            str(app["category_id"]) for app in batch if app["id"] == id
        ][0]
        page["category"] = [app["category"] for app in batch if app["id"] == id][0]
        page["rating"] = response["ratingAverage"]
        page["reviews"] = response["totalNumberOfReviews"]
        page["ratings"] = response["ratingCount"]
        page["onestar"] = response["ratingCountList"][0]
        page["twostar"] = response["ratingCountList"][1]
        page["threestar"] = response["ratingCountList"][2]
        page["fourstar"] = response["ratingCountList"][3]
        page["fivestar"] = response["ratingCountList"][4]
        self.content.append(page)
