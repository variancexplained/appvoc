#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Fileapp_name   : /appvoc/scraper/appvoc/http/review.py                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 10th 2023 05:01:05 am                                                  #
# Modified   : Wednesday August 9th 2023 04:35:34 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppVoC Review Request Module"""
from __future__ import annotations
import logging

import pandas as pd
from dependency_injector.wiring import Provide, inject

from appvoc.data.acquisition.rating.result import RatingResult
from appvoc.data.acquisition.rating.validator import RatingValidator
from appvoc.infrastructure.web.headers import STOREFRONT
from appvoc.container import AppVoCContainer
from appvoc.infrastructure.web.asession import ASessionHandler


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
        session_handler: ASessionHandler = Provide[AppVoCContainer.web.asession],
        batch_size: int = 5,
    ) -> None:
        self._apps = apps
        self._session_handler = session_handler
        self._batch_size = batch_size
        self._batch = 0
        self._batches = []
        self._num_batches = 0
        self._url = None
        self._header = STOREFRONT["headers"]

        self.create_batches()

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def create_batches(self) -> None:
        self._batches = self._create_batches()
        self._num_batches = len(self._batches)

    async def scrape(self) -> RatingResult:
        """Sends the next batch of urls to the session handler and parses the response.

        Return: RatingResult object, containing projects and results in DataFrame format.
        """
        for batch_idx in range(self._num_batches):
            validator = RatingValidator()
            result = RatingResult()

            responses = await self._session_handler.get(
                urls=self._batches[batch_idx]["urls"], headers=self._header
            )

            batch = self._batches[batch_idx]["apps"]
            for response in responses:
                if validator.is_valid(response=response):
                    result.add_response(response=response, batch=batch)
                else:
                    result.data_errors += validator.data_error
                    result.client_errors += validator.client_error
                    result.server_errors += validator.server_error
            yield result

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
            if idx % self._batch_size == 0 or idx == len(app_dict):
                batch = {"apps": apps, "urls": urls}
                batches.append(batch)
                apps = []
                urls = []
        return batches
