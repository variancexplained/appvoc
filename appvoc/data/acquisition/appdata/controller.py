#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# AppDataProject    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/data/acquisition/appdata/controller.py                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 05:23:40 pm                                                  #
# Modified   : Sunday June 30th 2024 02:01:39 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppVoC Scraper AppDataProject Module"""
import datetime
import logging
import sys
from typing import Union

from dependency_injector.wiring import Provide, inject

from appvoc.container import AppVoCContainer
from appvoc.data.acquisition.app.project import AppDataProject
from appvoc.data.acquisition.app.result import AppDataResponse
from appvoc.data.acquisition.app.scraper import AppDataScraper
from appvoc.data.repo.uow import UoW


# ------------------------------------------------------------------------------------------------ #
#                            APPSTORE APP DATA CONTROLLER                                          #
# ------------------------------------------------------------------------------------------------ #
class AppDataController:
    """AppVoC App Data Controller encapsulates a scraping project.

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
        uow: UoW = Provide[AppVoCContainer.data.uow],
        scraper: type[AppDataScraper] = AppDataScraper,
        max_pages: int = sys.maxsize,
        max_results_per_page: int = 200,
        verbose: int = 10,
        backup_to_file: bool = True,
        failure_threshold: int = 10,
    ) -> None:
        self._uow = uow
        self._scraper = scraper
        self._verbose = verbose
        self._max_pages = max_pages
        self._max_results_per_page = max_results_per_page
        self._backup_to_file = backup_to_file
        self._failure_threshold = failure_threshold

        # Stats
        self._page = 0
        self._pages = 0
        self._apps = 0
        self._rate = 0
        self._started = None
        self._duration = None
        self._failures = 0

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def archive(self) -> None:
        """Saves the repository to an archive"""
        self.uow.app_repo.export()

    def scrape(self, terms: Union[str, list]) -> None:
        """Implementation of the Scrape AppDataProject"""

        terms = [terms] if isinstance(terms, str) else terms

        for term in terms:
            self._execute_project(term)

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
                if result.is_valid():
                    project.update(apps=len(result.content))
                    self._persist(result, project)
                    self._update_report_stats(project)
                else:
                    self._failures += 1

                if self._failures >= self._failure_threshold:
                    self._failures = 0
                    break

            self._complete_project(project)

    def _get_or_start_project(self, term: str) -> AppDataProject:
        """Returns a new or existing project for the term

        Args:
            term (str): The search term
        """
        self._started = datetime.datetime.now()
        try:
            project = self._uow.app_project_repo.get_project(
                controller=self.__class__.__name__,
                term=term,
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
            self._uow.app_project_repo.load(project)
            self._uow.save()

            msg = f"\n\nStarted project for {term.capitalize()} apps."
            self._logger.info(msg)
        elif project.status == "complete":
            msg = f"\n\nProject for {term.capitalize()} apps is complete."
            self._logger.info(msg)

        else:
            msg = f"\n\nResuming project for {term.capitalize()} from page {project.get_start_page()}"
            self._logger.info(msg)

        return project

    def _persist(self, result: AppDataResponse, project: AppDataProject) -> None:
        """Persists the results in the repository, and updates the project."""
        self._uow.app_repo.load(result.content)
        self._uow.app_project_repo.update(data=project)
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
        self._uow.app_project_repo.update(data=project)
        self._uow.save()

        # Run dedup
        self._uow.app_repo.dedup()

        # If backing up,  save the repo to archive.
        if self._backup_to_file:
            self._uow.app_repo.export()
        msg = f"Completed AppDataProject: \n{project}\n"
        self._logger.info(msg)
