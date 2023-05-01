#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/appstore/appdata/controller.py                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 05:23:40 pm                                                  #
# Modified   : Sunday April 30th 2023 06:51:49 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Scraper Project Module"""
import os
import sys
import logging
from dotenv import load_dotenv
import datetime
from typing import Union

import pandas as pd
from dependency_injector.wiring import Provide, inject

from aimobile.data.acquisition.base import Controller
from aimobile.data.acquisition.appstore.appdata.scraper import AppStoreAppDataScraper
from aimobile.data.acquisition.project import Project
from aimobile.data.repo.uow import UoW
from aimobile.container import AIMobileContainer


# ------------------------------------------------------------------------------------------------ #
#                            APPSTORE APP DATA CONTROLLER                                          #
# ------------------------------------------------------------------------------------------------ #
class AppStoreAppDataController(Controller):
    """AppStore App Data Controller encapsulates a scraping project.

    Args:
        scraper (AppStoreAppScraper): A scraper object that returns data from the target urls.
        uow (UoW): Unit of Work class containing references to all Repos
        max_pages (int): The maximum number of pages to process.
        verbose (int): Indicates progress reporting verbosity in terms of the number of pages
            between progress reports to the log.

    """

    @inject
    def __init__(
        self,
        uow: UoW = Provide[AIMobileContainer.data.uow],
        scraper: type[AppStoreAppDataScraper] = AppStoreAppDataScraper,
        max_pages: int = sys.maxsize,
        max_results_per_page: int = 200,
        verbose: int = 10,
    ) -> None:
        super().__init__()
        self._uow = uow
        self._scraper = scraper
        self._verbose = verbose
        self._max_pages = max_pages
        self._max_results_per_page = max_results_per_page

        # Stats
        self._page = 0
        self._pages = 0
        self._apps = 0
        self._rate = 0
        self._started = None
        self._duration = None

        self._host = "itunes.apple.com"

        self._project = None
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def scrape(self, terms: Union[str, list]) -> None:
        """Scrapes app data matching the search term from the target URL.

        Args:
            terms (Union[str,list]): Search term or a list of search terms.
        """
        load_dotenv()
        status = os.getenv("APPSTORE_DATA_SCRAPED")
        if status in [True, "True", "true"]:
            msg = "\n\nAppstore AppData Scraped Status is Complete. Skipping App Store App Data Scraping Operation."
            self._logger.info(msg)
        else:
            self._scrape(terms=terms)

        self._teardown()

    def summarize(self) -> pd.DataFrame:
        """Returns a DataFrame summarizing the data extracted"""
        return self.uow.appdata_repository.summarize()

    def archive(self) -> None:
        """Saves the repository to an archive"""
        self.uow.appdata_repository.export()

    def _scrape(self, terms: Union[str, list]) -> None:
        """Implementation of the Scrape Project"""
        terms = [terms] if isinstance(terms, str) else terms

        for term in terms:
            start_page = self._start_project(term)

            for scraper in self._scraper(
                term=term,
                page=start_page,
                max_pages=self._max_pages,
                limit=self._max_results_per_page,
            ):
                self._update_project(scraper.result)
                self._announce(term=term)

            self._end_project()

    def _start_project(self, term: str) -> int:
        """Determines start page, and creates the term Project object."""
        project = self._get_project_if_exists(term)

        start_page = self.start_project(term)
        self._pages = 0
        self._apps = 0
        self._rate = 0
        return start_page

    def _update_project(self, result: pd.DataFrame) -> None:
        # Update project stats
        self._pages += 1
        self._apps += result.shape[0]
        seconds = (datetime.datetime.now() - self._started).total_seconds()
        self._duration = str(datetime.timedelta(seconds=seconds))
        self._rate = round(self._apps / seconds, 2)
        # Persist project and results
        self.update_project(self._pages)
        self.uow.appdata_repository.add(data=result)
        self.uow.save()

    def _end_project(self, pages: int) -> None:
        self.complete_project()
        self.uow.appdata_repository.export()

    def _announce(self, term: str) -> None:
        if self._pages % self._verbose == 0:
            msg = f"Term: {term.capitalize()}\tScrapers: {self._pages}\tApps: {self._apps}\tElapsed Time: {self._duration}\tRate: {self._rate} apps per second."
            self._logger.info(msg)

    def _get_project_if_exists(self, term: str) -> Union[Project, None]:
        """Obtains the most recent Project object for the term from the repo if one exists."""
        # Category is synonymous with term.
        controller = self.__class__.__name__
        repo = self._uow.project_repo.get_project(controller=controller, term=term)
