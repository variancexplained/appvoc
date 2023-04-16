#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/service/reviews.py                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 02:44:42 pm                                                 #
# Modified   : Saturday April 15th 2023 08:38:12 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Reviews Scraper Module"""
import logging

import pandas as pd
from dependency_injector.wiring import Provide, inject

from aimobile.scraper.appstore.entity.project import AppStoreProject
from aimobile.scraper.appstore.repo.datacentre import DataCentre
from aimobile.scraper.appstore.http.review import AppStoreReviewRequest
from aimobile.scraper.base import AbstractReviewScraper
from aimobile.scraper.appstore.container import AppStoreContainer
from aimobile.scraper.appstore.http.base import Handler
from aimobile.scraper.appstore.entity.base import AppStoreCategoryIds
from aimobile.scraper.appstore.http.base import HTTPVars


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

    @property
    def project(self) -> AppStoreProject:
        return self._project

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
                if request:
                    self._logger.info(
                        f"\n\nScraped {request.result.shape[0]} reviews for app #: {self._total_apps}, App: {row['id']} - {row['name']}"
                    )
                    self._update_stats(row=row, reviews=request.results)
                    self._persist(request)
                else:
                    break

        # Close the project
        self._teardown()
        self.summarize()

    def _setup(self, category_id: int = None) -> pd.DataFrame:
        """Some initialization and returns all apps for a category_id."""
        self._category_id = category_id
        self._category = AppStoreCategoryIds.NAMES[category_id]
        self._setup_project(category_id)
        return self._get_apps(category_id)

    def _setup_project(self, category_id: int) -> None:
        """Creates the project and saves it in the repository"""
        name = str(category_id) + "-" + AppStoreCategoryIds.NAMES.get(category_id)
        self._project = AppStoreProject(name=name)
        self._project.start()
        self._datacentre.project_repository.add(project=self._project)

    def _get_apps(self, category_id: int) -> pd.DataFrame:
        """Obtains the all app ids and names for the category id"""
        apps = self._datacentre.appdata_repository.get_by_category(category_id=category_id)
        msg = f"Apps in category: {apps.shape[0]}"
        self._logger.info(msg)
        try:
            reviewed = self._datacentre.review_repository.get_by_category(category_id=category_id)
            msg = f"App reviews obtained: {reviewed.shape[0]}"
            self._logger.info(msg)
        except Exception:
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

        # Update project and persist
        self._project.update(num_results=request.results, content_length=request.content_length)
        self._datacentre.project_repository.update(project=self._project)

        # Save request object
        self._datacentre.request_repository.add(request.request)
        self._datacentre.save()

    def _teardown(self) -> None:
        """Some final bookeeping."""
        self._project.end()
        # Set the status to success, unless an exception has occurred and
        # post the project to the database and release the resources.
        self._datacentre.project_repository.update(self._project)

    def summarize(self) -> dict:
        """Summarizes the scraping operation."""
        d = {
            "Class": self.__class__.__name__,
            "Category Id:": self._category_id,
            "Category:": self._category,
            "First App Id:": self._first_app_id,
            "First App Name:": self._first_app_name,
            "Last App Id:": self._last_app_id,
            "Last App Name:": self._last_app_name,
            "Total Apps:": self._total_apps,
            "Total Reviews:": self._total_reviews,
        }
        print(
            f"{self.__class__.__name__}\n\tCategory: {self._category_id} - {self._category}\n\tFirst App: {self._first_app_id} - {self._first_app_name}\n\tLast App: {self._last_app_id} - {self._last_app_name}\n\tTotal Apps: {self._total_apps}\n\tTotal Reviews: {self._total_reviews}"
        )
        return d
