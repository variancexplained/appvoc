#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/service/ratings.py                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 15th 2023 07:44:25 pm                                                #
# Modified   : Sunday April 16th 2023 03:26:55 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Appstore App Ratings Service Module"""
import logging

from tqdm import tqdm
import pandas as pd
from dependency_injector.wiring import Provide, inject

from aimobile.scraper.appstore.repo.datacentre import DataCentre
from aimobile.scraper.appstore.http.review import AppStoreRatingsRequest
from aimobile.scraper.base import AbstractRatingsScraper
from aimobile.scraper.appstore.container import AppStoreContainer
from aimobile.scraper.appstore.http.base import Handler
from aimobile.scraper.appstore.entity.base import AppStoreCategoryIds


# ------------------------------------------------------------------------------------------------ #
class AppStoreRatingsScraper(AbstractRatingsScraper):
    """App Store Ratingss Scraper

    This class implements the methods to retrieve app rating information from the itunes app store.

    Args:
        request (type[AppStoreRatingsRequest]): A request object that specifies the request
            parameters and defines the process for parsing the request response.
        session_handler (Handler): Handles the session that performs the request, managing
            retries as defined in the session handler object.
        datacentre (AppStoreDataCentre): Manages the project, request and app data
            repositories under single database context.
    """

    @inject
    def __init__(
        self,
        request: type[AppStoreRatingsRequest] = AppStoreRatingsRequest,
        session_handler: Handler = Provide[AppStoreContainer.session.handler],
        datacentre: DataCentre = Provide[AppStoreContainer.datacentre.repo],
    ) -> None:
        self._request = request
        self._session_handler = session_handler
        self._datacentre = datacentre

        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def search(self, category_id: int) -> None:
        """Executes a search of app rating data, and persists the results in the appstore ratings repository.

        Args:
            category_id (int): An app category id from AppStoreCategories

        """
        app_ratings = []
        # Initialize the project and obtain the list of app ids.
        apps = self._setup(category_id)

        for _, row in tqdm(apps.iterrows()):
            request = self._request.get_ratings(app_id=row["id"])
            if request.status_code == 200:
                app_ratings.append(request.result)

        app_ratings = pd.DataFrame(app_ratings)
        self._persist(app_ratings)

    def _setup(self, category_id: int = None) -> pd.DataFrame:
        """Some initialization and returns all apps for a category_id."""
        self._category_id = category_id
        self._category = AppStoreCategoryIds.NAMES[category_id]
        return self._get_apps(category_id)

    def _get_apps(self, category_id: int) -> pd.DataFrame:
        """Obtains the all app ids for the category id"""
        apps = self._datacentre.appdata_repository.get_by_category(category_id=category_id)
        try:
            scraped = self._datacentre.ratings_repository.getall()
            apps = apps[~apps["id"].isin(scraped["id"])]
            return apps
        except Exception:
            return apps

    def _persist(self, app_ratings: pd.DataFrame) -> None:
        """Saves the app and project data to the database."""
        # Save review data
        self._datacentre.ratings_repository.add(data=app_ratings)

        # Commit the database.
        self._datacentre.save()
