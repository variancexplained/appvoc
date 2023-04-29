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
# Modified   : Saturday April 29th 2023 06:56:05 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Review Request Module"""
from __future__ import annotations
import logging
import requests

from dependency_injector.wiring import Provide, inject

from aimobile.data.acquisition.scraper.appstore import STOREFRONTS
from aimobile.container import AIMobileContainer
from aimobile.infrastructure.web.session import SessionHandler


# ------------------------------------------------------------------------------------------------ #
class AppStoreRatingScraper(RatingScraper):
    """App Store Rating Scraper

    Extracts review and rating count data by app_id

    Args
        apps (list): List of dictionaries containing:
            id: app_id
            name: app_name
            category_id: four digit IOS category
            category: the category name
        session (SessionHandler): Object that manages the HTTP requests
        max_invalid_responses (int): Maximum number of invalid responses in a row before
            terminating the iteration. Default = 5
    """

    @inject
    def __init__(
        self,
        apps=list,
        session: SessionHandler = Provide[AIMobileContainer.web.session],
        max_invalid_responses: int = 5,
    ) -> None:
        self._apps = apps
        self._session = session
        self._app_idx = 0
        self._max_invalid_responses = max_invalid_responses

        self._invalid_responses = 0
        self._host = "itunes.apple.com"
        self._url = None
        self._header = STOREFRONTS[0]["headers"]

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def __iter__(self) -> AppStoreRatingScraper:
        self._app_idx = 0
        return self

    def __next__(self) -> None:
        """Formats an itunes request for the next page.

        If we have an invalid response, we move on to the next app.
        If there are max_invalid_responses in a row, we terminate.
        """

        if self._invalid_responses < self._max_invalid_responses and self._app_idx < len(
            self._apps
        ):
            self._setup()

            session = self._session.get(url=self._url, header=self._header)

            if self._is_valid_response(session):
                response = self._parse_session(session)
                self._result = self._parse_response(response)
                self._app_idx += 1
                self._invalid_responses = 0
                return self
            else:
                self._app_idx += 1
                self._invalid_responses += 1
                return self
        else:  # pragma: no cover
            raise StopIteration

    def _setup(self) -> None:
        """Sets the request url"""
        app = self._apps[self._app_idx]
        self._url = (
            f"https://itunes.apple.com/us/customer-reviews/id{app['id']}?displayable-kind=11"
        )

    def _is_valid_response(self, session: SessionHandler) -> bool:
        """Evaluates response status code and content"""
        valid = True

        try:
            if session.status_code != 200:
                msg = f"Invalid Response: Status code = {session.status_code}."
                valid = False
            elif not isinstance(session.response, requests.Response):
                msg = f"Invalid Response: Response is of type {type(session.response)}."
                valid = False
            elif not isinstance(session.response.json(), dict):
                msg = f"Invalid Response: Response json is of type {type(session.response.json())}."
                valid = False
            elif len(session.response.json()) == 0:
                msg = "Invalid Response: Response json has zero length."
                valid = False

        except Exception as e:
            valid = False
            msg = f"Invalid Response. A {type(e)} exception occurred. \n{e}"

        if not valid:
            self._logger.debug(msg)
        return valid

    def _parse_response(self, response: requests.Response) -> dict:
        """Accepts a requests Response object and returns a Dictionary

        Args:
            response (requests.Response): A requests Response object.

        """
        response = response.json()
        name = self._apps[self._app_idx]["name"]
        category_id = self._apps[self._app_idx]["category_id"]
        category = self._apps[self._app_idx]["category"]
        result = {}
        try:
            result["id"] = response["adamId"]
            result["name"] = name
            result["category_id"] = category_id
            result["category"] = category
            result["rating"] = response["ratingAverage"]
            result["reviews"] = response["totalNumberOfReviews"]
            result["ratings"] = response["ratingCount"]
            result["onestar"] = response["ratingCountList"][0]
            result["twostar"] = response["ratingCountList"][1]
            result["threestar"] = response["ratingCountList"][2]
            result["fourstar"] = response["ratingCountList"][3]
            result["fivestar"] = response["ratingCountList"][4]
            result["source"] = self._host
            return result
        except KeyError as e:
            msg = f"KeyError: {e}\nResponse:\n{response}"
            self._logger.error(msg)
            return None

    def _parse_session(self, session: SessionHandler) -> requests.Response:
        """Extracts data from the sesion object"""
        self._status_code = int(session.response.status_code)
        return session.response
