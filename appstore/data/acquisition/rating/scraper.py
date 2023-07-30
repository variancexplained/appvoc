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
# Modified   : Friday July 28th 2023 04:51:01 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Review Request Module"""
from __future__ import annotations
import logging

import pandas as pd
from dependency_injector.wiring import Provide, inject

from appstore.data.acquisition.rating.result import RatingResult, RatingResponse
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
            raise StopAsyncIteration

        responses = await self._session.get(
            urls=self._batches[self._batch]["urls"], headers=self._header
        )

        result = RatingResult()  # result object that will contain the responses.

        result = self._parse_responses(responses=responses, result=result)
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

    def _parse_responses(self, responses: list, result: RatingResult) -> list:
        """Accepts responses in list format and returns a list of parsed responses.

        Args:
            responses (list): A list of Response objects.
            result (RatingResult): Object to which the responses will be added.

        """
        batch = self._batches[self._batch]["apps"]

        for response in responses:
            try:
                if "adamId" in response:
                    response = RatingResponse.create(batch=batch, response=response)
                    result.add_response(response=response)
            except Exception as e:
                msg = f"\nInvalid response. Encountered {type(e)} exception.\n{e}\nResponse: {response}"
                self._logger.debug(msg)

        return result
