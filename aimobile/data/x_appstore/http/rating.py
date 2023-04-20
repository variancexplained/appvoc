#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Fileapp_name   : /aimobile/scraper/appstore/http/review.py                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 10th 2023 05:01:05 am                                                  #
# Modified   : Wednesday April 19th 2023 04:44:38 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Review Request Module"""
from __future__ import annotations
import logging
import random

import requests

from aimobile.data.x_appstore.http.base import Handler, STOREFRONTS


# ------------------------------------------------------------------------------------------------ #
class AppStoreRatingRequest:
    def __init__(
        self,
        handler: Handler,
    ) -> None:
        self._handler = handler
        self._content_length = 0
        self._sessions = 1
        self._status_code = None
        self._result = None
        self._proxy = None

        self._host = "itunes.apple.com"
        self._url = None
        self._headers = None
        self._params = None

        self._status_code = None
        self._result = None
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    @property
    def host(self) -> int:
        """Returns the current page processed."""
        return self._host

    @property
    def url(self) -> int:
        """Returns the current page processed."""
        return self._url

    @property
    def status_code(self) -> int:
        """Returns the length of the response"""
        return self._status_code

    @property
    def result(self) -> int:
        """Returns result in DataFrame format."""
        return self._result

    def search(self, app_id: int) -> AppStoreRatingRequest:
        """Returns the rating counts for ratings 1-5"""
        self._setup(app_id=app_id)

        session = self._handler.get(url=self._url, headers=self._headers)

        if self._is_valid_session(session=session):
            self._result = {"id": app_id}

            response = self._parse_session(session=session)

            self._result.update(self._parse_response(response))

        return self

    def _setup(self, app_id: int) -> None:
        """Selects an English speaking Store Front and sets the URL and headers accordingly."""
        storefront = random.choice(STOREFRONTS)
        self._url = f"https://itunes.apple.com/{storefront['country']}/customer-reviews/id{app_id}?displayable-kind=11"
        self._headers = storefront["headers"]

    def _parse_session(self, session: Handler) -> requests.Response:
        """Extracts metadata from session object."""
        self._status_code = session.status_code
        return session.response

    def _parse_response(self, response: requests.Response) -> dict:
        """Accepts a requests Response object and returns a dictionary

        Args:
            response (requests.Response): A requests Response object.

        """
        result = response.json()
        ratings = {}
        for i in range(1, len(result["ratingCountList"]) + 1):
            key = "star_" + str(i)
            ratings[key] = result["ratingCountList"][i - 1]
        ratings["total_ratings"] = result["ratingCount"]
        ratings["total_reviews"] = result["totalNumberOfReviews"]
        ratings["source"] = self._host
        return ratings

    def _is_valid_session(self, session: Handler) -> bool:
        """Returns True if an requests.Response object was returned."""

        return session.status_code == 200 and isinstance(session.response, requests.Response)
