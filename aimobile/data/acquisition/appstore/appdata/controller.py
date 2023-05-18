#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# AppDataProject    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/appstore/appdata/controller.py                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 05:23:40 pm                                                  #
# Modified   : Sunday May 7th 2023 12:58:23 pm                                                     #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Scraper AppDataProject Module"""
import os
import sys
import logging
from dotenv import load_dotenv
import datetime
from typing import Union

from dependency_injector.wiring import Provide, inject

from aimobile.data.acquisition.base import Controller
from aimobile.data.acquisition.appstore.appdata.scraper import AppStoreAppDataScraper
from aimobile.data.acquisition.appstore.appdata.project import AppDataProject
from aimobile.data.acquisition.base import Result
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
        backup_to_file: bool = True,
    ) -> None:
        super().__init__()
        self._uow = uow
        self._scraper = scraper
        self._verbose = verbose
        self._max_pages = max_pages
        self._max_results_per_page = max_results_per_page
        self._backup_to_file = backup_to_file

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
        if status in [True, "True", "true"]:  # pragma: no cover
            msg = "\n\nAppstore AppData Scraped Status is Complete. Skipping App Store App Data Scraping Operation."
            self._logger.info(msg)
        else:
            self._scrape(terms=terms)

    def summary(self) -> AppDataProject:
        return self._project

    def archive(self) -> None:
        """Saves the repository to an archive"""
        self.uow.appdata_repo.export()

    def _scrape(self, terms: Union[str, list]) -> None:
        """Implementation of the Scrape AppDataProject"""
        terms = [terms] if isinstance(terms, str) else terms

        for term in terms:
            self._start_project(term)
            if self._project.status != "complete":
                start_page = self._project.get_start_page()
                for result in self._scraper(
                    term=term,
                    start_page=start_page,
                    max_pages=self._max_pages,
                    limit=self._max_results_per_page,
                ):
                    self._project.update(apps=len(result.content))
                    self._persist(result)
                    self._update_report_stats()

                self._complete_project()

            else:
                msg = f"Project for {term} is complete. Skipping ahead to next project"
                self._logger.info(msg)

    def _start_project(self, term: str) -> bool:
        """Creates a project, returns True or False if project is complete."""
        self._started = datetime.datetime.now()
        self._rate = 0  # Rate of apps returned

        self._project = self._check_existing(term)
        if self._project is None:
            # Create a new project and add it to the repo
            self._project = AppDataProject.start(
                host=self._host,
                controller=self.__class__.__name__,
                term=term,
                page_size=self._max_results_per_page,
            )
            self._uow.project_repo.add(data=self._project)
            self._uow.save()

    def _persist(self, result: Result) -> None:
        """Persists the results in the repository, and updates the project."""
        self._uow.appdata_repo.add(result.content)
        self._uow.project_repo.update(data=self._project)
        self._uow.save()

    def _update_report_stats(self) -> None:
        """Computes and reports basic performance stats"""
        seconds = (datetime.datetime.now() - self._started).total_seconds()
        self._duration = str(datetime.timedelta(seconds=seconds))
        self._rate = round(self._project.apps / seconds, 2)
        if self._project.pages % self._verbose == 0:
            msg = f"Term: {self._project.term.capitalize()}\tPages: {self._project.pages}\tApps: {self._project.apps}\tElapsed Time: {self._duration}\tRate: {self._rate} apps per second."
            self._logger.info(msg)

    def _complete_project(self) -> None:
        self._project.complete()
        self._uow.project_repo.update(data=self._project)
        self._uow.save()

        # If backing up,  save the repo to archive.
        if self._backup_to_file:
            self._uow.appdata_repo.export()
        msg = f"Completed AppDataProject: \n{self._project}\n"
        self._logger.info(msg)

    def _check_existing(self, term: str) -> Union[AppDataProject, None]:
        """If the project exists, return it.

        Args:
            term (str): The project search term.

        """
        controller = self.__class__.__name__
        try:
            return self._uow.project_repo.get_project(controller=controller, term=term)
        except Exception:  # pragma: no cover
            return None
