#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/appstore/service/appdata.py                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 02:44:17 pm                                                 #
# Modified   : Tuesday April 18th 2023 11:15:10 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore App Details Scraper Module"""
import logging

from dependency_injector.wiring import Provide, inject

from aimobile.data.appstore.repo.datacentre import DataCentre
from aimobile.data.appstore.http.appdata import AppStoreSearchRequest
from aimobile.data.base import AbstractAppDataScraper
from aimobile.framework.container import AppStoreContainer
from aimobile.data.appstore.http.base import Handler


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
        datacentre: DataCentre = Provide[AppStoreContainer.datacentre.repo],
    ) -> None:
        self._request = request
        self._session_handler = session_handler
        self._datacentre = datacentre
        self._page = None
        self._pages = 0
        self._results = 0

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

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
                self._announce(request=request, verbose=verbose)

    def _setup(self, term: str, page: int) -> None:
        """Some initialization"""
        self._term = term
        self._page = page
        self._pages = 0
        self._results = 0
        self._total_results = 0

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

        # Commit changes to the repositories.
        self._datacentre.save()

    def _announce(self, request: AppStoreSearchRequest, verbose: int) -> None:
        if self._pages % verbose == 0:
            term = self._term.capitalize()
            msg = f"Term: {term} - Page {self._page} returned {self._results} for a total of {self._total_results} returned. Pages returned: {self._pages}. App id: {request.result['id'][0]} thru {request.result['id'].iloc[-1]}"
            self._logger.info(msg)
