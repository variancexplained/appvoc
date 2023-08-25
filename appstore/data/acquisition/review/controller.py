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
# Modified   : Thursday August 24th 2023 08:19:25 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Scraper Controller Module"""
import sys
import logging

import pandas as pd
from dependency_injector.wiring import inject, Provide

from appstore.data.acquisition.review.scraper import ReviewScraper
from appstore.data.acquisition.review.director import ReviewDirector
from appstore.data.acquisition.review.job import ReviewJobRun
from appstore.data.acquisition.review.result import ReviewResult
from appstore.data.acquisition.review.request import ReviewRequest
from appstore.data.repo.uow import UoW
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
        director: type[ReviewDirector] = ReviewDirector,
        scraper: type[ReviewScraper] = ReviewScraper,
        uow: UoW = Provide[AppstoreContainer.data.uow],
        failure_threshold: int = 10,
        min_ratings: int = 20,
        max_pages: int = sys.maxsize,
        max_results_per_page: int = 400,
        verbose: int = 10,
    ) -> None:
        super().__init__()
        self._scraper = scraper
        self._director = director(uow=uow)
        self._uow = uow
        self._failure_threshold = failure_threshold
        self._min_ratings = min_ratings
        self._max_pages = max_pages
        self._max_results_per_page = max_results_per_page
        self._verbose = verbose
        self._failures = 0

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def scrape(self) -> None:
        """Entry point for scraping operation"""
        if not super().is_locked():
            self._scrape()
        else:  # pragma: no cover
            msg = f"Running {self.__class__.__name__} is not authorized at this time."
            self._logger.info(msg)

    def _scrape(self) -> None:
        """Driver for scraping operation."""
        jobrun = self._director.next()
        while jobrun is not None:
            jobrun = self.start_jobrun(jobrun=jobrun)
            apps = self._get_apps(category_id=jobrun.category_id)

            if len(apps) > 0:
                for app_idx, row in apps.iterrows():
                    app = self._get_app(row=row)
                    request = self._get_or_create_request_log(app=app)
                    jobrun.apps += 1

                    for result in self._scraper(
                        app=app,
                        max_pages=self._max_pages,
                        max_results_per_page=self._max_results_per_page,
                        start=request.last_index,
                    ):
                        if result.is_valid():
                            self._failures = 0
                            self.persist(result)
                            jobrun = self.update_jobrun(jobrun=jobrun, result=result)
                            request.last_index = result.index
                        else:
                            self._failures += 1

                        if self._failures >= self._failure_threshold:  # pragma: no cover
                            self._failures = 0
                            break

                    self._uow.review_request_repo.update(request=request)

                    if app_idx % self._verbose == 0:
                        jobrun.announce()

            self.end_jobrun(jobrun=jobrun)
            jobrun = self._director.next()

    def _get_app(self, row: pd.Series) -> App:
        return App(
            id=row["id"],
            name=row["name"],
            category_id=row["category_id"],
            category=row["category"],
        )

    def _get_apps(self, category_id: int) -> pd.DataFrame:
        # Obtain all apps for the category from the repository.
        apps = self._uow.appdata_repo.get_by_category(category_id=category_id)
        msg = f"\n\nA total of {len(apps)} apps in category {category_id}."

        # Filter the apps that have greater than 'min_ratings'
        # This is a proxy for number of potential reviews.
        apps = apps.loc[apps["ratings"] > self._min_ratings]

        if len(apps) > 0:
            msg += f"\nApps to process: {len(apps)}"
            self._logger.info(msg)
        else:  # pragma: no cover
            msg += f"No apps meet minimum ratings criteria in category {category_id}"
            self._logger.info(msg)
        return apps

    def _get_or_create_request_log(self, app: App) -> ReviewRequest:
        """Gets existing or creates new review request object."""
        try:
            request = self._get_request_log(app=app)
            if request is not None:
                return request
            else:
                return self._create_request_log(app=app)
        except Exception:
            return self._create_request_log(app=app)

    def _get_request_log(self, app: App) -> ReviewRequest:
        return self._uow.review_request_repo.get(id=app.id)

    def _create_request_log(self, app: App) -> ReviewRequest:
        request = ReviewRequest(id=app.id, category_id=app.category_id)
        self._uow.review_request_repo.add(request=request)
        return request

    def persist(self, result: ReviewResult) -> None:
        """Persists results to Database

        Args:
            result (ReviewResult) -> Parsed result object
        """
        self._uow.review_repo.load(data=result.get_result())
        self._uow.save()

    def start_jobrun(self, jobrun: ReviewJobRun) -> ReviewJobRun:
        """Starts a jobrun and adds a jobrun to the repository.

        Args:
            jobrun (ReviewJobRun): The current job run.

        """
        jobrun.start()
        self._director.add_jobrun(jobrun=jobrun)
        return jobrun

    def update_jobrun(self, jobrun: ReviewJobRun, result: ReviewResult) -> ReviewJobRun:
        """Adds results to jobrun, and persists.

        Args:
            jobrun (ReviewJobRun): The current job run.
            result (ReviewResult): The result from the scraping operation

        """
        jobrun.add_result(result=result)
        self._director.update_jobrun(jobrun=jobrun)
        return jobrun

    def end_jobrun(self, jobrun: ReviewJobRun) -> None:
        """Persists job to the Database

        Args:
            result (ReviewResult) -> Parsed result object
        """
        jobrun.end()
        # Get the associated job and end it.
        job = self._uow.job_repo.get(id=jobrun.jobid)
        job.end(completed=jobrun.completed)
        # Persist the jobrun and the job.
        self._director.update_job(job=job)
        self._director.update_jobrun(jobrun=jobrun)
        # Archive the ratings
        self._uow.rating_repo.export()
