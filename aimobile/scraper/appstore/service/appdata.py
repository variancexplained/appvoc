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
# Modified   : Saturday April 15th 2023 11:56:30 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore App Details Scraper Module"""
import logging

from dependency_injector.wiring import Provide, inject

from aimobile.scraper.appstore.entity.project import AppStoreProject
from aimobile.scraper.appstore.repo.datacentre import DataCentre
from aimobile.scraper.appstore.http.appdata import AppStoreSearchRequest
from aimobile.scraper.base import AbstractAppDataScraper
from aimobile.scraper.appstore.container import AppStoreContainer
from aimobile.scraper.appstore.http.base import Handler


# ------------------------------------------------------------------------------------------------ #
class AppStoreScraper(AbstractAppDataScraper):
    """iTunes App Store scraper

    This class implements methods to retrieve information about iTunes App
    Store apps in various ways. Much has been adapted from the itunes-app-scraper,
    which can be found at  https://github.com/digitalmethodsinitiative/itunes-app-scraper

    Args:
        request (type[AppStoreSearchRequest]): A request object that specifies the request
            parameters and defines the process for parsing the request response.
        session_handler (Handler): Handles the session that performs the request, managing
            retries as defined in the session handler object.
        datacentre (AppStoreDataCentre): Manages the project, request and app data
            repositories under single database context.
    """

    @inject
    def __init__(
        self,
        request: type[AppStoreSearchRequest] = AppStoreSearchRequest,
        session_handler: Handler = Provide[AppStoreContainer.session.handler],
        datacentre: DataCentre = Provide[AppStoreContainer.datacentre.repo],
    ) -> None:
        self._request = request
        self._session_handler = session_handler
        self._datacentre = datacentre
        self._project = None
        self._page = None
        self._pages = 0
        self._results = 0

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def project(self) -> AppStoreProject:
        return self._project

    def search(
        self, term: str, page: int = 0, max_pages: int = None, limit: int = None, verbose: int = 10
    ) -> None:
        """Executes a search of app data, and persists the results in the appstore appdate repository.

        Args:
            term (str): Search term.
            page (int): Starting page
            max_pages (int): The maximum number of pages to return
            limit (int): The maximum number of results to return per page.
            verbose (int): Indicates the degree of progress reporting. Progress will be
                reported to standard after each 'verbose' page requests.

        """
        # Initialize the project.
        self._setup(term=term, page=page)

        # Iterate over our requests iterator
        for request in self._request(
            term=term, page=page, max_pages=max_pages, limit=limit, handler=self._session_handler
        ):
            if request.status_code == 200:
                self._update_stats(request=request)
                self._persist(request=request)
                self._announce(term=term, request=request, verbose=verbose)

        # Close the project
        self._teardown()

    def _setup(self, term: str, page: int) -> None:
        """Some initialization"""
        self._page = page
        self._pages = 0
        self._results = 0
        self._total_results = 0
        self._project = AppStoreProject(name=term)
        self._project.start()
        self._datacentre.project_repository.add(project=self._project)

    def _update_stats(self, request: AppStoreSearchRequest) -> None:
        """Updates progress metadata."""
        self._page += 1
        self._pages += 1
        self._results = request.results
        self._total_results += request.results

    def _persist(self, request: AppStoreSearchRequest) -> None:
        """Saves the app and project data to the database."""
        # Save App data
        self._datacentre.appdata_repository.add(data=request.result)

        # Update project and persist
        self._project.update(num_results=request.results, content_length=request.content_length)
        self._datacentre.project_repository.update(project=self._project)

        # Save request object
        self._datacentre.request_repository.add(request.request)
        self._datacentre.save()

    def _announce(self, term: str, request: AppStoreSearchRequest, verbose: int) -> None:
        if self._pages % verbose == 0:
            term = term.capitalize()
            msg = f"Term: {term} - Page {self._page} returned {self._results} for a total of {self._total_results} returned. Pages returned: {self._pages}. App id: {request.result['id'][0]} thru {request.result['id'].iloc[-1]}"
            self._logger.info(msg)

    def _teardown(self) -> None:
        """Some final bookeeping."""
        self._project.end()
        # Set the status to success, unless an exception has occurred and
        # post the project to the database and release the resources.
        self._datacentre.project_repository.update(self._project)

    def summarize(self) -> None:
        """Prints a summary of the appdata scraping project."""
        print(self._project)
