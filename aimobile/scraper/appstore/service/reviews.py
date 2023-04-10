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
# Modified   : Monday April 10th 2023 12:35:02 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Reviews Scraper Module"""
import logging
import requests

import pandas as pd
from dependency_injector.wiring import Provide, inject

from aimobile.scraper.appstore.entity.project import AppStoreProject
from aimobile.scraper.appstore.repo.datacentre import DataCentre
from aimobile.scraper.appstore.http.reviews import AppStoreReviewRequest
from aimobile.scraper.base import AbstractReviewScraper
from aimobile.scraper.appstore.container import AppStoreContainer
from aimobile.scraper.appstore.http.base import Handler
from aimobile.scraper.appstore.entity.base import AppStoreCategoryIds


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

        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    @property
    def project(self) -> AppStoreProject:
        return self._project

    def search(self, category_id: int, max_pages: int = None) -> None:
        """Executes a search of app data, and persists the results in the appstore appdate repository.

        Args:
            category_id (int): An app category id from AppStoreCategories
            page (int): The starting page.
            max_pages (int): The maximum number of pages to return

        """
        # Initialize the project and obtain the list of app ids.
        app_count = 0
        apps = self._setup(category_id)

        for _, row in apps.iterrows():
            app_count += 1
            self._logger.debug(
                f"\n\nScraping reviews for app #: {app_count}, App Id: {row['id']} - App Name: {row['name']}"
            )
            try:
                # Iterate over our requests iterator
                for request in self._request(
                    id=row["id"],
                    name=row["name"],
                    category_id=row["category_id"],
                    category=row["category"],
                    max_pages=max_pages,
                    handler=self._session_handler,
                ):
                    self._persist(request)
            except requests.exceptions.JSONDecodeError:
                msg = "Encountered a json error, implying the end of reviews for this app."
                self._logger.debug(msg)

        # Close the project
        self._teardown()

    def _setup(self, category_id: int = None) -> None:
        """Some initialization"""
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
        return self._datacentre.appdata_repository.get_category(category_id=category_id)

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

    def summarize(self) -> None:
        """Prints a summary of the appdata scraping project."""
        print(self._project)
