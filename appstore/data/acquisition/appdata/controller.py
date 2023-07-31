#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# AppDataProject    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/appdata/controller.py                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 05:23:40 pm                                                  #
# Modified   : Sunday July 30th 2023 11:59:23 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Scraper AppDataProject Module"""
import sys
import logging
import datetime
from typing import Union

from dependency_injector.wiring import Provide, inject

from appstore.data.acquisition.base import Controller
from appstore.data.acquisition.appdata.scraper import AppDataScraper
from appstore.data.acquisition.appdata.project import AppDataProject
from appstore.data.acquisition.appdata.result import AppDataResult
from appstore.data.storage.uow import UoW
from appstore.container import AppstoreContainer


# ------------------------------------------------------------------------------------------------ #
#                            APPSTORE APP DATA CONTROLLER                                          #
# ------------------------------------------------------------------------------------------------ #
class AppDataController(Controller):
    """AppStore App Data Controller encapsulates a scraping project.

    Note: Authorization is required to run controllers.

    Args:
        scraper (AppScraper): A scraper object that returns data from the target urls.
        uow (UoW): Unit of Work class containing references to all Repos
        max_pages (int): The maximum number of pages to process.
        verbose (int): Indicates progress reporting verbosity in terms of the number of pages
            between progress reports to the log.

    """

    @inject
    def __init__(
        self,
        uow: UoW = Provide[AppstoreContainer.data.uow],
        scraper: type[AppDataScraper] = AppDataScraper,
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

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def archive(self) -> None:
        """Saves the repository to an archive"""
        self.uow.appdata_repo.export()

    def scrape(self, terms: Union[str, list]) -> None:
        """Implementation of the Scrape AppDataProject"""
        if super().scrape():
            terms = [terms] if isinstance(terms, str) else terms

            for term in terms:
                self._execute_project(term)
        else:
            msg = f"Running {self.__class__.__name__} is not authorized at this time."
            self._logger.info(msg)

    def _execute_project(self, term: str) -> None:
        """Creates, executes and completes a project for the search term

        Args:
            term (str): Search term
        """

        project = self._get_or_start_project(term)
        if project is not None:
            start_page = project.get_start_page()
            for result in self._scraper(
                term=project.term,
                start_page=start_page,
                max_pages=self._max_pages,
                limit=self._max_results_per_page,
            ):
                project.update(apps=len(result.content))
                self._persist(result, project)
                self._update_report_stats(project)

            self._complete_project(project)

    def _get_or_start_project(self, term: str) -> AppDataProject:
        """Returns a new or existing project for the term

        Args:
            term (str): The search term
        """
        self._started = datetime.datetime.now()
        try:
            project = self._uow.appdata_project_repo.get_project(
                controller=self.__class__.__name__, term=term
            )
            msg = f"\nRetrieved Project:\n{str(project)}"
            self._logger.info(msg)

        except Exception:
            project = None

        if project is None:
            project = AppDataProject.start(
                controller=self.__class__.__name__,
                term=term,
                page_size=self._max_results_per_page,
            )
            self._uow.appdata_project_repo.add(project)
            self._uow.save()

            msg = f"\n\nStarted project for {term.capitalize()} apps."
            self._logger.info(msg)
        elif project.status == "complete":
            msg = f"\n\nProject for {term.capitalize()} apps is complete."
            self._logger.info(msg)

        else:
            msg = (
                f"\n\nResuming project for {term.capitalize()} from page {project.get_start_page()}"
            )
            self._logger.info(msg)

        return project

    def _persist(self, result: AppDataResult, project: AppDataProject) -> None:
        """Persists the results in the repository, and updates the project."""
        self._uow.appdata_repo.add(result.content)
        self._uow.appdata_project_repo.update(data=project)
        self._uow.save()

    def _update_report_stats(self, project: AppDataProject) -> None:
        """Computes and reports basic performance stats"""
        seconds = (datetime.datetime.now() - self._started).total_seconds()
        self._duration = str(datetime.timedelta(seconds=seconds))
        self._rate = round(project.apps / seconds, 2)
        if project.pages % self._verbose == 0:
            msg = f"Term: {project.term.capitalize()}\tPages: {project.pages}\tApps: {project.apps}\tElapsed Time: {self._duration}\tRate: {self._rate} apps per second."
            self._logger.info(msg)

    def _complete_project(self, project: AppDataProject) -> None:
        project.complete()
        self._uow.appdata_project_repo.update(data=project)
        self._uow.save()

        # If backing up,  save the repo to archive.
        if self._backup_to_file:
            self._uow.appdata_repo.export()
        msg = f"Completed AppDataProject: \n{project}\n"
        self._logger.info(msg)
