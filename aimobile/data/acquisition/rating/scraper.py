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
# Modified   : Thursday May 18th 2023 03:27:37 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Review Request Module"""
from __future__ import annotations
from datetime import datetime
import logging

import pandas as pd
from dependency_injector.wiring import Provide, inject

from aimobile.data.acquisition.rating.result import RatingResult
from aimobile.infrastructure.web.headers import STOREFRONT
from aimobile.container import AIMobileContainer
from aimobile.infrastructure.web.asession import ASessionHandler


# ------------------------------------------------------------------------------------------------ #
class AppStoreRatingScraper:
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
        session: ASessionHandler = Provide[AIMobileContainer.web.asession],
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

    def __aiter__(self) -> AppStoreRatingScraper:
        self._batch = 0
        self._batches = self._create_batches()
        return self

    async def __anext__(self) -> RatingResult:
        """Sends the next batch of urls to the session handler and parses the response.

        Return: RatingResult object, containing projects and results in DataFrame format.
        """

        if self._batch == len(self._batches):
            raise StopIteration

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

        ids_found = []
        results = []
        projects = []
        for response in responses:
            try:
                id = [app["id"] for app in apps if app["id"] == response["adamId"]][0]
                name = [app["name"] for app in apps if app["id"] == response["adamId"]][0]
                category_id = [
                    app["category_id"] for app in apps if app["id"] == response["adamId"]
                ][0]
                category = [app["category"] for app in apps if app["id"] == response["adamId"]][0]
                ids_found.append(id)
            except Exception as e:
                msg = f"\nInvalid response. Encountered {type(e)} exception. No project or result created.\n{e}"
                self._logger.error(msg)
                break

            result = {}
            project = {}
            try:
                project["id"] = self._batch
                project["app_id"] = response["adamId"]
                project["app_name"] = name
                project["category_id"] = category_id
                project["category"] = category
                project["created"] = datetime.now()
                project["status"] = "success"
                projects.append(project)

            except Exception as e:
                msg = f"\nInvalid response. Encountered {type(e)} exception. No project or result created.\n{e}"
                self._logger.error(msg)
                break
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
                results.append(result)

            except Exception as e:
                msg = (
                    f"\nInvalid response. Encountered {type(e)} exception. No result created.\n{e}"
                )
                self._logger.error(msg)

        for app in apps:
            if app["id"] not in ids_found:
                project = {}
                project["id"] = self._batch
                project["app_id"] = app["id"]
                project["app_name"] = app["name"]
                project["category_id"] = app["category_id"]
                project["category"] = app["category"]
                project["created"] = datetime.now()
                project["status"] = "fail"
                projects.append(project)
                msg = f"Request failed on app {app['id']}-{app['name']} of {app['category_id']}-{app['category']}. Adding to Projects."
                self._logger.error(msg)

        projects = pd.DataFrame(data=projects)
        results = pd.DataFrame(data=results)
        result = RatingResult(
            scraper=self.__class__.__name__,
            projects=projects,
            results=results,
        )
        return result
