#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Fileapp_name   : /appstore/scraper/appstore/http/review.py                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 10th 2023 05:01:05 am                                                  #
# Modified   : Thursday July 27th 2023 03:41:45 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Review Request Module"""
from __future__ import annotations
import logging

import pandas as pd
from dependency_injector.wiring import Provide, inject

from appstore.data.acquisition.rating.result import RatingResult
from appstore.infrastructure.web.headers import STOREFRONT
from appstore.container import AppstoreContainer
from appstore.infrastructure.web.asession import ASessionHandler


# ------------------------------------------------------------------------------------------------ #
class RatingScraper:
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
        apps=pd.DataFrame,
        session: ASessionHandler = Provide[AppstoreContainer.web.asession],
        batch_size: int = 5,
    ) -> None:
        self._apps = apps
        self._session = session
        self._batch_size = batch_size
        self._batch = 0
        self._batches = []

        self._invalid_responses = 0
        self._url = None
        self._header = STOREFRONT["headers"]

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def __aiter__(self) -> RatingScraper:
        self._batch = 0
        self._batches = self._create_batches()
        return self

    async def __anext__(self) -> RatingResult:
        """Sends the next batch of urls to the session handler and parses the response.

        Return: RatingResult object, containing projects and results in DataFrame format.
        """

        if self._batch == len(self._batches):
            return False

        responses = await self._session.get(
            urls=self._batches[self._batch]["urls"], headers=self._header
        )

        result = self._parse_responses(responses=responses)
        self._batch += 1
        return result

    def _create_batches(self) -> list:
        """Creates batches of URLs from a list of app ids"""
        batches = []
        apps = []
        urls = []
        app_dict = self._apps.to_dict(orient="index")

        for idx, app in enumerate(app_dict.values(), start=1):
            url = f"https://itunes.apple.com/us/customer-reviews/id{app['id']}?displayable-kind=11"
            apps.append(app)
            urls.append(url)
            if idx % self._batch_size == 0:
                batch = {"apps": apps, "urls": urls}
                batches.append(batch)
                apps = []
                urls = []
        return batches

    def _parse_responses(self, responses: list) -> list:
        """Accepts responses in list format and returns a list of parsed responses.

        Args:
            responses (list): A list of Response objects.

        """
        apps = self._batches[self._batch]["apps"]

        results = []
        total = 0
        success = 0
        fail = 0
        for response in responses:
            total += 1
            result = {}

            try:
                result["id"] = response["adamId"]
                result["name"] = [app["name"] for app in apps if app["id"] == response["adamId"]][0]
                result["category_id"] = [
                    app["category_id"] for app in apps if app["id"] == response["adamId"]
                ][0]
                result["category"] = [
                    app["category"] for app in apps if app["id"] == response["adamId"]
                ][0]
                result["rating"] = response["ratingAverage"]
                result["reviews"] = response["totalNumberOfReviews"]
                result["ratings"] = response["ratingCount"]
                result["onestar"] = response["ratingCountList"][0]
                result["twostar"] = response["ratingCountList"][1]
                result["threestar"] = response["ratingCountList"][2]
                result["fourstar"] = response["ratingCountList"][3]
                result["fivestar"] = response["ratingCountList"][4]
                result["status"] = True
                success += 1
                results.append(result)

            except Exception as e:
                result["id"] = response["adamId"]
                result["name"] = [app["name"] for app in apps if app["id"] == response["adamId"]][0]
                result["category_id"] = [
                    app["category_id"] for app in apps if app["id"] == response["adamId"]
                ][0]
                result["category"] = [
                    app["category"] for app in apps if app["id"] == response["adamId"]
                ][0]
                result["rating"] = 0
                result["reviews"] = 0
                result["ratings"] = 0
                result["onestar"] = 0
                result["twostar"] = 0
                result["threestar"] = 0
                result["fourstar"] = 0
                result["fivestar"] = 0
                result["status"] = False
                fail += 1
                results.append(result)

                msg = f"\nInvalid response. Encountered {type(e)} exception.\n{e}\n{response}"
                self._logger.debug(msg)

        results = pd.DataFrame(data=results)
        result = RatingResult(
            scraper=self.__class__.__name__,
            results=results,
            total=total,
            success=success,
            fail=fail,
        )
        return result
