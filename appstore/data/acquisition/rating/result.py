#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/rating/result.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 01:59:31 pm                                                  #
# Modified   : Tuesday August 1st 2023 10:28:20 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Result Object for Rating Responses"""
from __future__ import annotations
from dataclasses import dataclass

from appstore.data.acquisition.base import Result
from appstore.infrastructure.web.utils import getsize


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RatingResult(Result):
    """Encapsulates the review results. Inherits the following from Result base class:
    content (list): List of dictionaries containing the response content
    size: (int): Total size of response in bytes
    requests (int): Number of requests. This will be one for syncronous requests,
        async requests vary.
    successes: (int): Number of successful responses
    errors: (int): Number of errors.

    """

    apps: int = 0

    def add_response(self, content: dict) -> None:
        """Adds a rating to the result content

        Args:
           review (dict): Dictionary containing review data
        """
        self.content.append(content)
        self.size += getsize()
        self.apps += 1
