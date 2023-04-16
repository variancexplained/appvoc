#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Fileapp_name   : /aimobile/scraper/appstore/http/reviews.py                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 10th 2023 05:01:05 am                                                  #
# Modified   : Sunday April 16th 2023 04:42:08 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Review Request Module"""
from __future__ import annotations
import logging
import re
import random

import requests

from aimobile.scraper.appstore.http.base import Handler, STOREFRONTS
from aimobile.scraper.appstore.entity.request import AppStoreRequest


# ------------------------------------------------------------------------------------------------ #
class Regex:
    STARS = re.compile(r"<span class=\"total\">[\s\S]*?</span>")


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
        self._request = None
        self._requested = None
        self._responded = None
        self._response_time = None
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
    def content_length(self) -> int:
        """Returns the length of the response"""
        return self._content_length

    @property
    def sessions(self) -> int:
        """Returns the length of the response"""
        return self._sessions

    @property
    def status_code(self) -> int:
        """Returns the length of the response"""
        return self._status_code

    @property
    def request(self) -> AppStoreRequest:
        return self._request

    @property
    def result(self) -> int:
        """Returns result in DataFrame format."""
        return self._result

    @property
    def requested(self) -> int:
        """Datetime string at which the request was made."""
        return self._requested

    @property
    def responded(self) -> int:
        """Datetime string at which the response was received."""
        return self._responded

    @property
    def response_time(self) -> int:
        """Response time in microseconds."""
        return self._response_time

    @property
    def proxy(self) -> str:
        """Returns the proxy server used."""
        return self._proxy

    def get_ratings(self, app_id: int) -> AppStoreRatingRequest:
        """Returns the rating counts for ratings 1-5"""
        self._setup(app_id=app_id)

        session = self._handler.get(url=self._url, headers=self._headers)

        self._request = self._create_request_object()

        if self._is_valid_session(session=session):
            self._result = {"id": app_id}

            response = self._parse_session(session=session)

            self._result.update(self._parse_response(response))

        return self

    def _setup(self, app_id: int) -> None:
        """Initializes the iterator"""
        self._content_length = 0
        self._status_code = None
        self._result = None
        self._proxy = None
        # randomly select matching english speaking country and headers
        storefront = random.choice(STOREFRONTS)
        self._url = f"https://itunes.apple.com/{storefront['country']}/customer-reviews/id{app_id}?displayable-kind=11"
        self._headers = storefront["headers"]

    def _parse_session(self, session: Handler) -> requests.Response:
        """Extracts metadata from session object."""
        self._status_code = session.status_code
        self._requested = session.requested
        self._responded = session.responded
        self._response_time = session.response_time
        self._content_length = session.content_length
        self._sessions = session.sessions
        self._proxy = session.proxy
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

    def _create_request_object(self) -> AppStoreRatingRequest:
        """Creates the request object"""
        data = {
            "host": self._host,
            "name": self._app_id,
            "content_length": self._content_length,
            "results": self._results,
            "requested": self._requested,
            "responded": self._responded,
            "response_time": self._response_time,
            "sessions": self._sessions,
            "proxy": self._proxy,
            "status_code": self._status_code,
        }

        return AppStoreRequest.from_dict(data=data)

    def _is_valid_session(self, session: Handler) -> bool:
        """Returns True if an requests.Response object was returned."""

        return session.status_code == 200 and isinstance(session.response, requests.Response)
