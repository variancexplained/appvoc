#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Controller    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/review/controller.py                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday April 20th 2023 05:33:57 am                                                #
# Modified   : Wednesday August 2nd 2023 08:38:27 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Scraper Controller Module"""
import sys
import logging
from datetime import datetime

import pandas as pd
from dependency_injector.wiring import inject, Provide

from appstore.data.acquisition.review.scraper import ReviewScraper
from appstore.data.acquisition.review.director import ReviewDirector
from appstore.data.acquisition.review.job import ReviewJobRun
from appstore.data.acquisition.review.result import ReviewResult
from appstore.data.storage.uow import UoW
from appstore.data.acquisition.base import Controller, App
from appstore.container import AppstoreContainer


# ------------------------------------------------------------------------------------------------ #
#                            APPSTORE REVIEW CONTROLLER                                            #
# ------------------------------------------------------------------------------------------------ #
class ReviewController(Controller):
    """Controls the App Store Review scraping process

    Args:
        scraper (ReviewScraper): A scraper object that returns data from the target urls.
        uow (UoW): Unit of Work containing the repositories.
        min_ratings (int): Since we want apps with a minimum number of reviews, and we don't
            have the number of reviews per app, we are using the number of ratings as
            a proxy for the number of reviews. The default is 20
        max_pages (int): Puts a maximum on the total number of pages to request.
        max_results_per_page (int): This is the limit of results to return on each request.
        verbose (int): An indicator of the level of progress reporting verbosity. Progress
            will be printed to stdout for each 'verbose' number of apps processed.

    """

    @inject
    def __init__(
        self,
        scraper: type[ReviewScraper] = ReviewScraper,
        director: ReviewDirector = Provide[AppstoreContainer.director.review],
        uow: UoW = Provide[AppstoreContainer.data.uow],
        min_ratings: int = 20,
        max_pages: int = sys.maxsize,
        max_results_per_page: int = 400,
        verbose: int = 10,
    ) -> None:
        super().__init__()
        self._scraper = scraper
        self._director = director
        self._uow = uow
        self._min_ratings = min_ratings
        self._max_pages = max_pages
        self._max_results_per_page = max_results_per_page
        self._verbose = verbose

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def scrape(self) -> None:
        """Entry point for scraping operation"""
        if not super().is_locked():
            self._scrape()
        else:
            msg = f"Running {self.__class__.__name__} is not authorized at this time."
            self._logger.info(msg)

    def _scrape(self) -> None:
        """Driver for scraping operation."""

        for jobrun in self._director:
            if jobrun is not None:
                self._logger.debug(jobrun)
                jobrun.start()
                apps = self._get_apps(category_id=jobrun.category_id)
                self._logger.debug(apps)
                if len(apps) > 0:
                    for _, row in apps.iterrows():
                        app = App(
                            id=row["id"],
                            name=row["name"],
                            category_id=row["category_id"],
                            category=row["category"],
                        )
                        jobrun.apps += 1

                        for result in self._scraper(
                            app=app,
                            max_pages=self._max_pages,
                            max_results_per_page=self._max_results_per_page,
                        ):
                            if result.is_valid():
                                self.persist(result)
                                self.update_jobrun(jobrun, result)

                            if jobrun.apps % self._verbose == 0:
                                jobrun.announce()

                    self.end_jobrun(jobrun)

    def _get_apps(self, category_id: int) -> pd.DataFrame:
        # Obtain all apps for the category from the repository.
        apps = self._uow.appdata_repo.get_by_category(category_id=category_id)
        msg = f"\n\nA total of {len(apps)} apps in category {category_id}."

        # Filter the apps that have greater than 'min_ratings' ratings
        # This is a proxy for number of potential reviews.
        apps = apps.loc[apps["ratings"] > self._min_ratings]

        # Obtain apps for which we've already processed the reviews.
        try:
            reviews = self._uow.review_repo.get_by_category(category_id=category_id)
            apps_with_reviews = reviews["app_id"].unique()
        except Exception:
            apps_with_reviews = []

        # Remove apps for which reviews exist from the list of apps to process.
        if apps_with_reviews > 0:
            apps = apps.loc[~apps["id"].isin(apps_with_reviews)]

        if len(apps) > 0:
            msg += f"\nApps remaining: {len(apps)}"
            self._logger.info(msg)
        else:
            msg += f"All apps have been processed for category: {category_id}"
            self._logger.info(msg)
        return apps

    def persist(self, result: ReviewResult) -> None:
        """Persists results to Database

        Args:
            result (ReviewResult) -> Parsed result object
        """
        self._uow.review_repo.add(data=result.get_result())
        self._uow.save()

    def update_jobrun(self, jobrun: ReviewJobRun, result: ReviewResult) -> None:
        jobrun.add_result(result=result)
        self._uow.review_jobrun_repo.update(jobrun=jobrun)
        self._uow.save()

    def end_jobrun(self, jobrun: ReviewJobRun) -> None:
        """Persists job to the Database

        Args:
            result (ReviewResult) -> Parsed result object
        """
        jobrun.end()
        self._uow.review_jobrun_repo.update(jobrun=jobrun)
        job = self._uow.job_repo.get(id=jobrun.jobid)
        job.completed = datetime.now()
        job.complete = True
        self._uow.job_repo.update(job=job)
        self._uow.review_repo.archive()
        self._uow.save()
