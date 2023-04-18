#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/appstore/service/review.py                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 02:44:42 pm                                                 #
# Modified   : Tuesday April 18th 2023 11:14:56 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Reviews Scraper Module"""
import logging

import pandas as pd
from dependency_injector.wiring import Provide, inject

from aimobile.data.appstore.repo.datacentre import DataCentre
from aimobile.data.appstore.http.review import AppStoreReviewRequest
from aimobile.data.base import AbstractReviewScraper
from aimobile.framework.container import AppStoreContainer
from aimobile.data.appstore.http.base import Handler
from aimobile.data.appstore.entity.base import AppStoreCategoryIds
from aimobile.data.appstore.http.base import HTTPVars


# ------------------------------------------------------------------------------------------------ #
class AppStoreReviewScraper(AbstractReviewScraper):
    """App Store Reviews Scraper

    This class implements methods to retrieve information about iTunes App
    Store apps in various ways. Much has been adapted from the itunes-app-scraper,
    which can be found at  https://github.com/digitalmethodsinitiative/itunes-app-scraper

    Args:
        request (type[AppStoreReviewRequest]): A request object that specifies the request
            parameters and defines the process for parsing the request response.
        session_handler (Handler): Handles the session that performs the request, managing
            retries as defined in the session handler object.
        datacentre (AppStoreDataCentre): Manages the project, request and app data
            repositories under single database context.
    """

    @inject
    def __init__(
        self,
        request: type[AppStoreReviewRequest] = AppStoreReviewRequest,
        session_handler: Handler = Provide[AppStoreContainer.session.handler],
        datacentre: DataCentre = Provide[AppStoreContainer.datacentre.repo],
    ) -> None:
        self._request = request
        self._session_handler = session_handler
        self._datacentre = datacentre
        self._project = None

        self._category_id = None
        self._category = None
        self._first_app_id = None
        self._first_app_name = None
        self._last_app_id = None
        self._last_app_name = None
        self._total_apps = 0
        self._total_reviews = 0

        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def search(self, category_id: int, max_pages: int = HTTPVars.MAX_PAGES) -> None:
        """Executes a search of app data, and persists the results in the appstore appdate repository.

        Args:
            category_id (int): An app category id from AppStoreCategories
            page (int): The starting page.
            max_pages (int): The maximum number of pages to return


        """
        # Initialize the project and obtain the list of app ids.
        apps = self._setup(category_id)

        for _, row in apps.iterrows():
            self._total_apps += 1

            # Iterate over our requests iterator
            for request in self._request(
                app_id=row["id"],
                app_name=row["name"],
                category_id=row["category_id"],
                category=row["category"],
                max_pages=max_pages,
                handler=self._session_handler,
            ):
                if request.status_code == 200:
                    self._logger.info(
                        f"\n\nScraped {request.result.shape[0]} reviews for app #: {self._total_apps}, App: {row['id']} - {row['name']}"
                    )
                    self._update_stats(row=row, reviews=request.results)
                    self._persist(request)
                else:
                    break  # pragma: no cover

    def _setup(self, category_id: int = None) -> pd.DataFrame:
        """Some initialization and returns all apps for a category_id."""
        self._category_id = category_id
        self._category = AppStoreCategoryIds.NAMES[category_id]
        return self._get_apps(category_id)

    def _get_apps(self, category_id: int) -> pd.DataFrame:
        """Obtains the all app ids and names for the category id"""
        apps = self._datacentre.appdata_repository.get_by_category(category_id=category_id)
        msg = f"Apps in category: {apps.shape[0]}"
        self._logger.info(msg)
        try:  # pragma: no cover
            reviewed = self._datacentre.review_repository.get_by_category(category_id=category_id)
            msg = f"App reviews obtained: {reviewed.shape[0]}"
            self._logger.info(msg)
        except Exception:  # pragma: no cover
            return apps
        apps = apps[~apps["id"].isin(reviewed["app_id"])]
        msg = f"Apps requiring review data: {apps.shape[0]}"
        self._logger.info(msg)
        return apps

    def _update_stats(self, row, reviews: int = 0) -> None:
        """Updates the statistics used in the summary."""
        self._total_reviews += reviews
        self._first_app_id = row["id"] if self._first_app_id is None else self._first_app_id
        self._first_app_name = row["name"] if self._first_app_name is None else self._first_app_name
        self._last_app_id = row["id"]
        self._last_app_name = row["name"]

    def _persist(self, request: AppStoreReviewRequest) -> None:
        """Saves the app and project data to the database."""
        # Save review data
        self._datacentre.review_repository.add(data=request.result)

        # Save request object
        self._datacentre.save()
