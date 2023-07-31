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
# Modified   : Sunday July 30th 2023 08:18:30 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Scraper Controller Module"""
import sys
import logging

from dependency_injector.wiring import inject, Provide

from appstore.data.acquisition.review.scraper import ReviewScraper
from appstore.data.acquisition.review.director import ReviewDirector
from appstore.data.acquisition.review.job import ReviewJob
from appstore.data.acquisition.review.result import ReviewResult
from appstore.data.storage.uow import UoW
from appstore.data.acquisition.base import Controller
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

        for job in self._director():
            apps = self.start_job(job=job)

            for idx, row in apps.iterrows():
                for page in self._scraper(
                    app_id=row["id"],
                    app_name=row["name"],
                    category_id=row["category_id"],
                    category=row["category"],
                    max_pages=self._max_pages,
                    max_results_per_page=self._max_results_per_page,
                ):
                    self._save_results(result=page.result)
                    job.update(result=page.result)
                    if idx % self._verbose == 0:
                        job.announce()

            self._end_job(job=job)

    def start_job(self, job: ReviewJob) -> None:
        # Obtain all apps for the category from the repository.
        frontier = {}
        frontier["category_id"] = job.category_id
        frontier["category"] = job.category
        apps = self._uow.appdata_repo.get_by_category(category_id=job.category_id)
        frontier["apps"] = len(apps)

        # Filter the apps that have greater than 'min_ratings' ratings
        # This is a proxy for number of potential reviews.
        apps = apps.loc[apps["ratings"] > self._min_ratings]
        frontier["apps_with_min_ratings"] = len(apps)

        # Obtain apps for which we've already processed the reviews.
        try:
            reviews = self._uow.review_repo.get_by_category(category_id=job.category_id)
            apps_with_reviews = reviews["app_id"].unique()
            frontier["apps_with_reviews"] = len(apps_with_reviews)
        except Exception:
            frontier["apps_with_reviews"] = 0

        # Remove apps for which reviews exist from the list of apps to process.
        if frontier["apps_with_reviews"] > 0:
            apps = apps.loc[~apps["id"].isin(apps_with_reviews)]
        frontier["apps_to_process"] = len(apps)

        self._announce_job_start(frontier=frontier)

        return apps

    def _announce_job_start(self, frontier: dict) -> None:
        width = 32
        msg = f"\n\nCategory: {frontier['category_id']}-{frontier['category']} Started at {frontier['started'].strftime('%m/%d/%Y, %H:%M:%S')}\n"
        msg += f"\t{'Apps in Category:'.rjust(width, ' ')} | {frontier['apps']}\n"
        msg += f"\t{'Apps with Min Ratings:'.rjust(width, ' ')} | {frontier['apps_with_min_ratings']}\n"
        msg += f"\t{'Apps with Reviews:'.rjust(width, ' ')} | {frontier['apps_with_reviews']}\n"
        msg += f"\t{'Apps to Process:'.rjust(width, ' ')} | {frontier['apps_to_process']}\n"
        self._logger.info(msg)

    def save_results(self, result: ReviewResult) -> None:
        """Persists results to Database

        Args:
            result (ReviewResult) -> Parsed result object
        """
        self._uow.review_repo.add(data=result.as_df())
        self._uow.save()

    def end_job(self, job: ReviewJob) -> None:
        """Persists job to the Database

        Args:
            result (ReviewResult) -> Parsed result object
        """
        job.end()
        self._uow.review_job_repo.update(job=job)
        self._uow.review_repo.archive()
