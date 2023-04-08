#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/service/appdata.py                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 02:44:17 pm                                                 #
# Modified   : Saturday April 8th 2023 03:31:43 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

import pandas as pd
from dependency_injector.wiring import Provide, inject

from aimobile.scraper.appstore.entity.project import AppStoreProject
from aimobile.scraper.appstore.repo.datacentre import DataCentre
from aimobile.scraper.appstore.internet.request import RequestIterator
from aimobile.scraper.base import AbstractAppDataScraper
from aimobile.scraper.appstore.container import AppStoreContainer


# ------------------------------------------------------------------------------------------------ #
class AppStoreScraper(AbstractAppDataScraper):
    """iTunes App Store scraper

    This class implements methods to retrieve information about iTunes App
    Store apps in various ways. Much has been adapted from the itunes-app-scraper,
    which can be found at  https://github.com/digitalmethodsinitiative/itunes-app-scraper

    Args:
        project (Project): The project definition, in terms of the search term, number of results
            per page, and maximum number of pages to scrape.
        country (str): Two letter country code. Default is 'us'
        lang (str): Two character language code. Default is 'en'
    """

    @inject
    def __init__(
        self,
        request: type[RequestIterator] = RequestIterator,
        datacentre: DataCentre = Provide[AppStoreContainer.datacentre.repo],
    ) -> None:
        self._request = request
        self._datacentre = datacentre
        self._request_iterator = None
        self._project = None

        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    @property
    def project(self) -> AppStoreProject:
        return self._project

    def search(self, term, max_pages: int = None, limit: int = None) -> None:
        """Executes a search of app data, and persists the results in the appstore appdate repository.

        Args:
            term (str): Search term.

        """
        # Initialize the request iterator and the project.
        self._setup(term)

        # Iterate over our requests iterator
        for result in self._request(term=term, max_pages=max_pages, limit=limit):
            self._persist(result)

        # Close the project
        self._teardown()

    def _setup(self, term: str = None) -> None:
        """Some initialization"""
        self._project = AppStoreProject(name=term)
        self._project.start()
        self._datacentre.project_repository.add(project=self._project)

    def _persist(self, result: pd.DataFrame) -> None:
        """Saves the app and project data to the database."""

        self._datacentre.appdata_repository.add(data=result)
        self._project.update(num_results=result.shape[0])
        self._datacentre.project_repository.update(project=self._project)
        self._datacentre.save()

    def _teardown(self) -> None:
        """Some final bookeeping."""
        self._project.end()
        # Set the status to success, unless an exception has occurred and
        # post the project to the database and release the resources.
        self._datacentre.project_repository.update(self._project)
        self._datacentre.close()
        self._datacentre.dispose()

    def summarize(self) -> None:
        """Prints a summary of the appdata scraping project."""
        self._project.summary()
